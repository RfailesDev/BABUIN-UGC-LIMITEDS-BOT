# Текст вызова команды, название вызываемой функции.
import this

def init():
    print("Commands ini")
    this.Commands.append(["Бабуин", "HelpCommand", "HelpCommand"])

    this.Commands.append(["Бабуин начни работу", "StartWork", "StartWork"])
    this.Commands.append(["Бабуин добавь лимитку", "AddLimit", "AddLimit"])  # После ":" не проверяет, по этому все ок
    this.Commands.append(["Бабуин покажи лимитки", "ShowLimits", "ShowLimits"])
    this.Commands.append(["Бабуин убери лимитку", "DeleteLimit", "DeleteLimit"])
    this.Commands.append(["Бабуин отключись", "TurnOff", "TurnOff"])
    this.Commands.append(["Бабуин вырубись", "TurnOff", "TurnOff"])
    this.Commands.append(["Бабуин +пауза", "Pause", "Pause"])
    this.Commands.append(["Бабуин -пауза", "StopPause", "StopPause"])
    this.Commands.append(["Бабуин что за предмет", "CheckItem", "CheckItem"])