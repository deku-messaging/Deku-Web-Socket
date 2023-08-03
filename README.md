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
"actions": "<Actions>"
}
```
- `MESSAGES_TYPE_SINGLE`: Single Thread has been requested
```json
{
"type": "MESSAGES_TYPE_SINGLE",
"threadId": "24",
"smsList": "[{<sms item>}, ...]",
"actions": "<Actions>"
}
```

### Global Actions
- `create`: New message has been added
- `read`: Message(s) or threads) can be rendered on UI

### SMS Type
- `1`:
