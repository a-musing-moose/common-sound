from mu.command.base import BaseCommand


class Moo(BaseCommand):

    group = "sound"

    def cow(self):
        return """
             \   ^__^
              \  (oo)\_______
                 (__)\       )\/\\
                     ||----w |
                     ||     ||
        """

    def bubble(self):
        return (
            "  ________________  \n"
            "< That's μ to you! >\n"
            "  ----------------  "
        )

    def execute(self, args, settings):
        print(self.bubble() + self.cow())
