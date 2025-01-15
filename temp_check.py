import subprocess
import argparse
import logging
import json
from datetime import datetime
import shutil

logging.basicConfig(
    filename="temp_check.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def istats_installation():
    if shutil.which("istats") is None:
        print("Please install iStats for this script to work. Command: 'sudo gem install iStats'.")
        return False
    return True

def cpu_temp():
    """Outputs CPU temperature using iStats."""
    try:
        logging.debug("Launching iStats command...")
        
        output = subprocess.check_output(["istats", "cpu", "temperature"]).decode("utf-8")
        logging.debug("Outputting CPU temperature.")
        for line in output.split("\n"):
                if "CPU temperature" in line:
                    temp = line.split(":")[1].strip().split(" ")[0]
                    logging.info(f"CPU temperature: {temp} C")
                    return temp
        logging.warning("CPU temperature failed in iStats.")
        return None
    except subprocess.CalledProcessError as e:
         logging.error("Subprocess call failed.", exc_info=True)
         return None
    except Exception as e:
         logging.error("An unknown error occured.", exc_info=True)
         return None
    
def format_temperature(temp, output_format):
    """Formats the temperature output based on the specified format."""
    if temp is None:
        return "Error: Could not retrieve CPU temperature."
    
    if output_format == "json":
        result = json.dumps({"CPU Temperature (°C)": temp})
    elif output_format == "verbose":
        result = f"The current CPU temperature is {temp} degrees Celsius."
    else:
        result = f"{temp}°C"
    return result

def main():
    parser = argparse.ArgumentParser(description="CLI tool to check CPU temperature on MacBook Air.")
    parser.add_argument(
        "-f", "--format", 
        choices=["plain", "verbose", "json"], 
        default="plain", 
        help="Output format: plain, verbose, or json"
    )
    parser.add_argument(
        "-l", "--log", 
        action="store_true", 
        help="Enable detailed logging in temp_check.log"
    )
    
    args = parser.parse_args()

    if args.log:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    logging.debug("Script started with arguments: %s", args)

    if not istats_installation():
        return

    temp = cpu_temp()
    formatted_output = format_temperature(temp, args.format)
    print(formatted_output)

if __name__ == "__main__":
    main()   
            
            
        