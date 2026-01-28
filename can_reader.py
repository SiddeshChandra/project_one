import cantools
import can
from cantools.database import errors as cantools_errors

def read_can_log(log_file, db_file):
    db = cantools.database.load_file(db_file)
    print(f"Loaded DBC file: {db_file}")

    print("\nCAN Log Messages:")
    with open(log_file, 'r') as f:
        for line in f:
            try:
                parts = line.strip().split(' ')
                if len(parts) >= 4 and parts[0] == 'can0': # Ensure it starts with 'can0' and has enough parts
                    arb_id_str = parts[1]
                    # DLC (parts[2]) is not directly used by cantools.decode_message, but we can log it if needed
                    data_hex_parts = parts[3:] # Get all data hex parts
                    data_hex = "".join(data_hex_parts)

                    arb_id = int(arb_id_str) # CAN ID is typically decimal in DBC, so parse as decimal
                    data = bytes.fromhex(data_hex)

                    try:
                        message_def = db.get_message_by_frame_id(arb_id)
                        decoded_message = message_def.decode(data)
                        print(f"  ID: {hex(arb_id)}, Data: {data_hex}, Decoded: {decoded_message}")
                    except KeyError as e:
                        print(f"  ID: {hex(arb_id)}, Data: {data_hex}, Message ID Error: {e} - ID not found in DBC.")
                    except cantools_errors.DecodeError as e:
                        print(f"  ID: {hex(arb_id)}, Data: {data_hex}, Decoding Error (cantools): {e}")
                    except Exception as e:
                        print(f"  ID: {hex(arb_id)}, Data: {data_hex}, General Error: {e}")
                else:
                    print(f"  Skipping malformed line: {line.strip()}")
            except Exception as e:
                print(f"  Error processing line '{line.strip()}': {e}")


if __name__ == "__main__":
    # Example usage
    log_file_path = "can.log"
    dbc_file_path = "temp.dbc"
    read_can_log(log_file_path, dbc_file_path)
