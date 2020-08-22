"""
This module houses the Messages class, which queues messages for consumption
by the react frontend.
"""


class Messages:
    """
    This class manages the message queue around delivering messages to separate
    clients, ensuring that each client gets all messages once and exactly once.
    """
    _clients = {}
    """ A dictionary used to store and lookup the message queues for each client
    """

    @staticmethod
    def add_message(msg_type, text):
        """
        Add the specified message to the queue for each client.

        :param msg_type: The type of message. One of 'track changed' or
                        'album queued'
        :param text: The message to display in the React front-end
        :return: None
        """
        [queue.append({'msg_type': msg_type, 'text': text})
         for queue in Messages._clients.values()]

    @staticmethod
    def ensure_client(ip):
        """
        Ensure this client exists and is registered for receiving messages.

        :param ip: The identifier used lookup and store messages in the queue
        :return: None
        """
        if ip not in Messages._clients.keys():
            Messages._clients[ip] = []

    @staticmethod
    def get_message(ip, state):
        """
        Add any outstanding messages for the specified IP to the payload.

        :param ip: The ip address of the client
        :param state: The state to add the message to (if required)
        :return: None
        """
        messages = Messages._clients[ip]
        if len(messages) > 0:
            state["message"] = messages.pop()