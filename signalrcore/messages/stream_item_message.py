from .base_message import BaseHeadersMessage
"""
A `StreamItem` message is a JSON object with the following properties:

* `type` - A `Number` with the literal value 2, indicating that this message is a `StreamItem`.
* `invocationId` - A `String` encoding the `Invocation ID` for a message.
* `item` - A `Token` encoding the stream item (see "JSON Payload Encoding" for details).

Example

```json
{
    "type": 2,
    "invocationId": "123",
    "item": 42
}
```
"""
class StreamItemMessage(BaseHeadersMessage):
    def __init__(
            self,
            message_type,
            headers
            invocation_id,
            item):
        super(StreamItemMessage, self).__init__(message_type, headers)
        self.invocation_id = invocation_id
        self.item = item
