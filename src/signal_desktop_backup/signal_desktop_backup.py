import os
from shutil import copyfile
import json
import sys
from sqlcipher3 import dbapi2 as sqlite
import hashlib
import regex as re
import json
import unicodedata
import time
from jinja2 import Environment, FileSystemLoader
import logging

logger = logging.getLogger("__file__")


def get_conversations(conn):

    #def _execute_query(query):
        #return 
    
    query = "SELECT id, name FROM conversations"

    return conn.execute(query).fetchall()


def get_messages(conn, conversation_id):
    return conn.execute(
        f"SELECT json FROM messages where conversationId='{id}' order by sent_at asc"
    ).fetchall()


class EncryptionKey:
    def __init__(self):
        self.e = None
        self.key = None

    def _get_keyfile(self, config_file):
        try:
            f = open(config_file, "r")
            logger.info(f"Opening config from {config_file}")
            return f is not None
        except FileNotFoundError as e:
            e.args = "Config file does not exist",
            self.e = e
    
    def _get_encryption_key_helper(self, config_file):
        try:
            file_exists = self._get_keyfile(config_file)
            if file_exists:
                with open(config_file, "r") as f:
                    data = f.read()
                    key = json.loads(data)["key"]
                    self.key = key
            
        except KeyError as e:
            e.args = "Encryption key is missing from config file",
            self.e = e

    def get_encryption_key(self, config_file):
        self._get_encryption_key_helper(config_file)
        if self.e:
            logger.debug(f"raising {type(self.e), self.e}")
            raise self.e
        return self.key


class SQLCipherConnection:
    def __init__(self, database, key):
        self.database = None
        self.key = None
        self.conn = self.get_connection()
        self.config = self.get_config()

    def get_config(self, version=4):
        if version == 4:
            return {
                "key": self.key,
                "cipher_page_size": 4096,
                "kdf_iter": 256000,
                "cipher_hmac_algorithm": "HMAC_SHA512",
                "cipher_kdf_algorithm": "PBKDF2_HMAC_SHA512",
            }
        else:
            raise NotImplementedError("Config needed for sqlite cipher 3")

    def get_connection(self):
        try:
            conn = sqlite.connect(self.database)
            self.conn = conn
        except sqlite.DatabaseError as e:
            self.e = e


def get_connection(database, key):
    try:
        print(f"Trying to open database {database} (using sqlcipher 4)")
        conn = sqlite.connect(database)
        c = conn.cursor()
        c.execute(f"PRAGMA key = \"x'{key}'\"")
        c.execute("PRAGMA cipher_page_size = 4096")
        c.execute("PRAGMA kdf_iter = 256000")
        c.execute("PRAGMA cipher_hmac_algorithm = HMAC_SHA512")
        c.execute("PRAGMA cipher_kdf_algorithm = PBKDF2_HMAC_SHA512")
        c.execute("SELECT * FROM sqlite_master").fetchall()
        return c
    except sqlite.OperationalError as e:
        print(f"OperationalError: {e}")
        sys.exit(1)
    except sqlite.DatabaseError as e:
        try:
            print(f"Trying to open database {database} (using sqlcipher 3)")
            conn = sqlite.connect(database)
            conn.execute("PRAGMA cipher_compatibility = 3")
            conn.execute("SELECT * FROM sqlite_master").fetchall()
            return conn
        except:
            print(f"DatabaseError: {e}")
            sys.exit(1)


def create_output_directory():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_directory = os.path.join(os.getcwd(), f"signal_export_{timestamp}")
    os.mkdir(output_directory)
    os.mkdir(os.path.join(output_directory, "conversations"))

    src = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "templates", "style.css"
    )
    dest = os.path.join(output_directory, "style.css")
    copyfile(src, dest)

    return output_directory


def _replace_unicode(s):
    def _replace(X):
        # return unicodedata.name(X.group())
        return re.sub(r"\s|$", "_", unicodedata.name(X.group()))
    # pattern = re.compile(r"(?P<ch>\X)")
    pattern = re.compile(r"[^-\w.]")
    return pattern.sub(_replace, s)


def _get_valid_filename(s):
    s = str(s).strip(r"\s\+#").strip("<3").replace(" ", "_")
    s = re.sub(r"\s|-", "_", s)
    return _replace_unicode(s)


def _hash_name(name):
    hashed = hashlib.md5(name.encode("utf-8")).hexdigest()
    return hashed


def get_conversation_filename(name):
    clean_name = _get_valid_filename(name)
    hashed = _hash_name(clean_name)
    return f"{clean_name}_{hashed}.html"


def create_html_index(conversations, export_dir, env):

    conversation_links = []
    for (id, name) in conversations:
        conversation_links.append((name, get_conversation_filename(id, name)))

    template = env.get_template("index.html")
    output = template.render(
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
        conversation_links=conversation_links,
    )

    with open(os.path.join(export_dir, "index.html"), "w") as output_file:
        output_file.write(output)
        output_file.close()


def parse_message_row(row_json):
    row = json.loads(row_json)

    if row.get("type") in ["incoming", "outgoing"]:
        mess_type = row.get("type")
    else:
        return None

    attachments = ""
    if "attachments" in row:
        for att in row.get("attachments"):
            attachments += "<br/>"
            if att.get("fileName") is not None:
                attachments += att.get("fileName")
            else:
                attachments += "[Filename unknown]"

    received = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(row["received_at"] / 1000)
    )
    body = row.get("body")

    return (mess_type, received, body, attachments)


def create_conversation_pages(conversations, output_directory, env):
    for (conversation_id, name) in conversations:
        print(f"Backing up '{name}'...")

        try:
            messages = get_messages(conn, conversation_id)
            message_data = []

            for json in messages:
                message_data.append(parse_message_row(json[0]))

            template = env.get_template("conversation.html")
            output = template.render(name=name, messages=message_data)

            with open(
                os.path.join(
                    output_directory,
                    "conversations",
                    get_conversation_filename(conversation_id, name),
                ),
                "w",
            ) as output_file:
                output_file.write(output)
                output_file.close()

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    print("Starting Signal Desktop export...")

    if sys.platform == "darwin":
        signal_data_path = os.path.join(
            os.path.expanduser("~"), "Library", "Application Support", "Signal"
        )
        config_file_path = os.path.join(signal_data_path, "config.json")
        database_file_path = os.path.join(signal_data_path, "sql", "db.sqlite")
    else:
        raise Exception("Only MacOS tested so far, extiting.") from TypeError
        sys.exit(0)

    conn = get_connection(database_file_path, EncryptionKey.get_encryption_key(config_file_path))
    output_directory = create_output_directory()

    conversations = get_conversations(conn)
    file_loader = FileSystemLoader(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    )
    env = Environment(loader=file_loader)

    create_html_index(conversations, output_directory, env)
    create_conversation_pages(conversations, output_directory, env)
