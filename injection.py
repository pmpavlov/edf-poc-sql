def injection(event, context):
  message = {
    'event': event,
    'task': context
  }

  return message
