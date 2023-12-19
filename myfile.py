from hiktools import sadp
from uuid import uuid4

# create a packet from a simple dict object
inquiry = sadp.fromdict({
  'Uuid': str(uuid4()).upper(),
  'MAC': 'ff-ff-ff-ff-ff-ff',
  'Types': 'inquiry'
})

# Open up a client to communicate over broadcast
with sadp.SADPClient() as client:
  # send the inquiry packet
  client.write(inquiry)

  # iterate over all received packets (None is returned on error)
  for response in client:
    if response is None: break
    # initiate the response
    message = sadp.unmarshal(response.toxml())

    # message objects contain a dict-like implementation
    # for property_name in message:
    #   print(message[property_name])

    # e.g.
    print('Device at', message['IPv4Address'])