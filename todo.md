# Functions

[x] get_conversations
[] get_messages
[x] get_encryption_key
[] get_connection

[x] create_output_directory
[x] _replace_unicode
[x] _get_valid_filename

[x] hash_name
[x] get_conversation_filename
[] create_html_index
[] parse_message_row
[] create_conversation_pages


I have 135 conversations {SELECT COUNT(*) FROM conversations}
and apparently 135 non-null IDs {SELECT COUNT( DISTINCT(id)) FROM conversations}.

7 group and 128 private chats