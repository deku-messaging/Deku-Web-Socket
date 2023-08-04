# Deku-Websocket-server

### SMS Item Body
```json
{
"address": "6505551212",
"body": "Android is always a sweet treat!",
"date": "1691010356892",
"displayName": null,
"errorCode": null,
"id": "367221886",
"read": 1,
"routerStatus": null,
 "routingUrls": [],
"statusCode": 0,
"subscriptionId": 0,
"threadId": "65",
"type": "<sms type>"
}
```

### Global Types
- `MESSAGES_TYPE_THREADS`: Threading list for messages
```json
{
"type": "MESSAGES_TYPE_THREADS",
"smsList": "[{<sms item>}, ...]",
"action": "<Actions>"
}
```
- `MESSAGES_TYPE_SINGLE`: Single Thread has been requested
```json
{
"type": "MESSAGES_TYPE_SINGLE",
"threadId": "24",
"smsList": "[{<sms item>}, ...]",
"action": "<Actions>"
}
```

### Global Actions
- `create`: New message has been added
- `read`: Message(s) or thread(s) can be rendered on UI
- `update`: Message(s) state has changed. State changes include `message sent`, `message failed`, `message delivered`. This would be determined by the SMS item `type`.
- `delete`: Message(s) or thread(s) have been deleted 

### SMS Type
- `1`: inbox
- `2`: sent
- `3`: dafts
- `4`: outbox
- `5`: failed
- `6`: queued
