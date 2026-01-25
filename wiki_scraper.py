from modules.cmd_interface import collect_cmd_args
from modules.controller import Controller

def main():
    args = collect_cmd_args()
    controller = Controller(args)
    controller.run()
    

if __name__ == "__main__":
    main()