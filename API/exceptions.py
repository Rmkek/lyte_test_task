class TicketRequestFailed(Exception):
    def __init__(self, message="Tickets are already sold out."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message