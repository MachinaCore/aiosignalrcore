from .base_message import BaseHeadersMessage

"""
A `Close` message is a JSON object with the following properties

* `type` - A `Number` with the literal value `7`,
    indicating that this message is a `Close`.
* `error` - An optional `String` encoding the error message.

Example - A `Close` message without an error
```json
{
    "type": 7
}
```

Example - A `Close` message with an error
```json
{
    "type": 7,
    "error": "Connection closed because of an error!"
}
```
"""


class CloseMessage(BaseHeadersMessage):
    def __init__(self, error: str, allow_reconnect: bool, **kwargs):
        super().__init__(7, **kwargs)
        self.error = error
        self.allow_reconnect = allow_reconnect
