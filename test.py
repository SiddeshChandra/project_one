import platform

def get_system_info():
    print(f"Operating System: {platform.system()}")
    print(f"Platform Version: {platform.version()}")
    print(f"Machine: {platform.machine()}")

if __name__ == "__main__":
    get_system_info()