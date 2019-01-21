import time


class Chrono:
    _nestedChronos = 0
    _nestedNewLines = 0

    """
    A class that implements a simple timer for the elapsed time, measured in millis.
    """

    def __init__(self, initial_message="Starting..."):
        self.initial_message = initial_message
        self.current_milli_time = lambda: int(round(time.time() * 1000))
        self.positionChrono = Chrono._nestedChronos
        self._start()

    def millis(self, final_message="done (in {} millis)"):
        self._print_final_message(final_message)

        self._stop()

    def get_millis(self):
        return self.current_milli_time() - self.start_time

    def _start(self):
        self._print_initial_message()

        self.start_time = self.current_milli_time()
        Chrono._nestedChronos += 1
        Chrono._nestedNewLines += 1

    def _stop(self):
        Chrono._nestedChronos -= 1
        if Chrono._nestedNewLines:
            Chrono._nestedNewLines -= 1

    def _print_initial_message(self):
        print(self._build_initial_message(), end="", flush=True)

    def _print_final_message(self, final_message):
        print(self._build_final_message(
            final_message.format(self.get_millis())), flush=True)

    def _build_initial_message(self, ):
        return self._start_prefix() + self.initial_message

    def _build_final_message(self, final_message):
        return self._final_prefix() + final_message

    def _start_prefix(self):
        s = ""
        if(Chrono._nestedNewLines > 0):
            s = "\n"
            Chrono._nestedNewLines -= 1
        return s + "\t" * Chrono._nestedChronos

    def _final_prefix(self):
        return "\t" if Chrono._nestedNewLines else "\t" * self.positionChrono


# import time
#
#
#
# class Chrono:
#     def __init__(self, initial_message, new_line = False,final_message="done"):
#         self.initial_message = initial_message
#         self.final_message = final_message
#         self.current_milli_time = lambda: int(round(time.time() * 1000))
#         self.start_time = self.current_milli_time()
#
#         print(initial_message, end="\n" if new_line else "", flush=True)
#
#     def end(self, message=None):
#         if message:
#             print("\t{}, {} (in {} millis)".format(self.final_message, message, self.current_milli_time() - self.start_time))
#         else:
#             print("\t{} (in {} millis)".format(self.final_message, self.current_milli_time() - self.start_time))
