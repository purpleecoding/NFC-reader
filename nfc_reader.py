import nfc
import sys
import binascii

# Callback for tag connection
def on_connect(tag):
    print("\n[INFO] Tag detected!")
    print(f"Tag type: {tag}")
    try:
        print(f"Tag UID: {tag.identifier.hex()}")
    except Exception:
        print("Could not read UID.")
    # Print all available tag info
    print("\n[INFO] Tag details:")
    for attr in dir(tag):
        if not attr.startswith('__') and not callable(getattr(tag, attr)):
            try:
                print(f"{attr}: {getattr(tag, attr)}")
            except Exception:
                pass
    print("\n[INFO] Tag __dict__:")
    print(tag.__dict__)
    # Try to dump NDEF records if available
    if hasattr(tag, 'ndef') and tag.ndef:
        print("\n[INFO] NDEF records:")
        for record in tag.ndef.records:
            print(record)
            print("Type:", record.type)
            print("Name:", record.name)
            print("Data:", record.data)
    else:
        print("No NDEF records found.")
    # Try to read memory blocks for common card types
    if hasattr(tag, 'dump'):
        print("\n[INFO] Memory dump:")
        try:
            dump = tag.dump()
            for i, block in enumerate(dump):
                print(f"Block {i}: {binascii.hexlify(block)}")
        except Exception as e:
            print(f"Could not dump memory: {e}")
    # Try to read data for Mifare/NTAG
    if tag.__class__.__name__ in ['MifareClassic', 'MifareUltralight', 'NDEFTag', 'Type2Tag']:
        print("\n[INFO] Attempting to read all memory blocks:")
        try:
            for page in range(0, 64):
                try:
                    data = tag.read(page)
                    print(f"Page {page}: {binascii.hexlify(data)}")
                except Exception:
                    break
        except Exception:
            pass
    return True  # Keep listening

def main():
    print("NFC Reader started. Press Ctrl+C to exit.")
    try:
        with nfc.ContactlessFrontend('usb') as clf:
            while True:
                clf.connect(rdwr={'on-connect': on_connect})
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
