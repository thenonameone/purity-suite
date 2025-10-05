# 🦆 Pure Pics BadUSB Workflow Guide

Complete guide for converting DuckyScript from Pure Pics to hardware BadUSB devices for automatic execution.

## 🎯 Overview

This workflow enables you to:
1. **Create** DuckyScript payloads in Pure Pics
2. **Convert** them to Arduino BadUSB code
3. **Deploy** on programmable USB hardware
4. **Execute** automatically when USB is inserted

---

## 🛠️ Tools Created

### 1. `ducky_to_badusb_converter.py`
**Main conversion tool** - Converts DuckyScript to Arduino sketches

```bash
# Basic usage
python3 ducky_to_badusb_converter.py -i script.txt -p arduino
python3 ducky_to_badusb_converter.py -i script.txt -p digispark

# Show hardware guide
python3 ducky_to_badusb_converter.py --guide
```

**Features:**
- ✅ Arduino Leonardo/Pro Micro support
- ✅ DigiSpark ATtiny85 support
- ✅ Proper key combination handling (GUI+R, CTRL+ALT+DEL)
- ✅ String escaping and special characters
- ✅ Comments preservation
- ✅ Error handling for unknown commands

### 2. `pure_pics_badusb_integration.py`
**Auto-monitoring tool** - Watches directories and auto-converts DuckyScript files

```bash
# Monitor home directory (auto-convert)
python3 pure_pics_badusb_integration.py --auto-convert

# Monitor specific directory with prompts
python3 pure_pics_badusb_integration.py --watch-dir /path/to/scripts --platform digispark

# Scan existing files only
python3 pure_pics_badusb_integration.py --scan-only --watch-dir /home/user
```

---

## 🔧 Hardware Setup

### Recommended Hardware

| **Device** | **Price** | **Pros** | **Cons** |
|------------|-----------|----------|----------|
| **Arduino Pro Micro** | ~$10 | Most reliable, well-supported | Larger size |
| **DigiSpark ATtiny85** | ~$5 | Tiny form factor, cheap | Limited memory |
| **Teensy LC** | ~$15 | Advanced features | Higher cost |

### Arduino Leonardo/Pro Micro Setup

1. **Install Arduino IDE**
   ```bash
   # Ubuntu/Debian
   sudo apt install arduino arduino-core
   
   # Or download from arduino.cc
   ```

2. **Board Configuration**
   - Tools → Board → Arduino Leonardo
   - Tools → Port → (select your device)

3. **Upload Process**
   - Open `.ino` file in Arduino IDE
   - Click Upload button
   - Device will auto-execute when plugged in

### DigiSpark ATtiny85 Setup

1. **Install DigiSpark Support**
   - File → Preferences → Additional Board Manager URLs
   - Add: `http://digistump.com/package_digistump_index.json`
   - Tools → Board → Boards Manager
   - Search and install "Digistump AVR Boards"

2. **Install DigiKeyboard Library**
   - Sketch → Include Library → Manage Libraries
   - Search "DigiKeyboard" and install

3. **Upload Process**
   - Tools → Board → DigiSpark (Default - 16.5MHz)
   - Click Upload
   - **Plug in DigiSpark when prompted** (within 60 seconds)

---

## 🚀 Complete Workflow

### Step 1: Create DuckyScript in Pure Pics
```bash
# Launch Pure Pics
python3 /home/xx/Pure_Pics.py
```
- Use the Rubber Ducky Script Editor
- Create/edit your payload
- Save the script to a text file

### Step 2: Convert to BadUSB
**Option A: Manual Conversion**
```bash
# Convert for Arduino
python3 ducky_to_badusb_converter.py -i my_script.txt -p arduino

# Convert for DigiSpark
python3 ducky_to_badusb_converter.py -i my_script.txt -p digispark
```

**Option B: Auto-monitoring**
```bash
# Start monitoring (will auto-convert Pure Pics output)
python3 pure_pics_badusb_integration.py --auto-convert --platform arduino
```

### Step 3: Upload to Hardware
1. Open generated `.ino` file in Arduino IDE
2. Select correct board and port
3. Upload sketch
4. Device is ready for deployment

### Step 4: Deploy and Execute
- Plug USB device into target system
- Payload executes automatically after ~2 second delay
- No user interaction required

---

## 📋 DuckyScript Conversion Examples

### Input DuckyScript:
```
REM Open PowerShell as Admin
DELAY 1000
GUI r
DELAY 500
STRING powershell
CTRL SHIFT ENTER
DELAY 2000
STRING Y
ENTER
```

### Arduino Output:
```cpp
void executePayload() {
  // Open PowerShell as Admin
  delay(1000);
  Keyboard.press(KEY_LEFT_GUI); Keyboard.press('r'); 
  Keyboard.release('r'); Keyboard.release(KEY_LEFT_GUI);
  delay(500);
  Keyboard.print("powershell");
  Keyboard.press(KEY_LEFT_CTRL); Keyboard.press(KEY_LEFT_SHIFT); 
  Keyboard.press(KEY_RETURN); Keyboard.release(KEY_RETURN); 
  Keyboard.release(KEY_LEFT_SHIFT); Keyboard.release(KEY_LEFT_CTRL);
  delay(2000);
  Keyboard.print("Y");
  Keyboard.press(KEY_RETURN); Keyboard.release(KEY_RETURN);
}
```

---

## ⚠️ Security & Legal Considerations

### 🛡️ Defense Evasion Tips
- **Test on isolated systems first**
- **Use realistic timing delays** (systems vary in boot/response time)
- **Consider USB device appearance** (use legitimate-looking cases)
- **Account for different keyboard layouts**
- **Test against antivirus/EDR solutions**

### 🔒 Modern Security Controls
Be aware these protections may block BadUSB attacks:
- **Device Control Policies** (Windows Defender, Enterprise policies)
- **USB Port Restrictions** (Physical/software blocks)
- **Script Execution Policies** (PowerShell, UAC prompts)
- **Endpoint Detection and Response** (EDR monitoring)
- **Application Whitelisting** (Only approved apps can run)

### ⚖️ Legal & Ethical Use
- **✅ Authorized penetration testing only**
- **✅ Educational research environments**
- **✅ Personal systems you own**
- **❌ Never use on systems without explicit permission**
- **❌ Illegal to deploy on others' systems**

---

## 🐛 Troubleshooting

### Common Issues

**1. Arduino IDE doesn't detect device**
```bash
# Check device permissions
ls -la /dev/ttyACM*
sudo usermod -a -G dialout $USER
# Logout and login again
```

**2. DigiSpark upload fails**
- Unplug DigiSpark before clicking Upload
- Plug in only when prompted
- Use high-quality USB cable
- Try different USB ports

**3. Payload doesn't execute**
- Check target system keyboard layout
- Increase initial delay (some systems boot slowly)
- Verify script syntax in original DuckyScript
- Test on isolated system first

**4. Characters appear wrong**
- Target may have different keyboard layout
- Consider using virtual key codes instead of strings
- Test with simple payloads first

### Debug Mode
Add debug output to your Arduino sketches:
```cpp
void setup() {
  Serial.begin(9600);
  Serial.println("BadUSB Payload Starting...");
  // ... rest of setup
}
```

---

## 📁 File Structure

After using the tools, you'll have:
```
/home/xx/
├── Pure_Pics.py                          # Main Pure Pics application
├── ducky_to_badusb_converter.py         # Conversion tool
├── pure_pics_badusb_integration.py      # Auto-monitoring
├── Pure_Pics_BadUSB_Workflow.md         # This guide
├── USB_AutoExecution_Methods.txt        # Detailed methods guide
└── Generated Files/
    ├── my_script.txt                     # Original DuckyScript
    ├── my_script_arduino.ino             # Arduino sketch
    ├── my_script_digispark.ino           # DigiSpark sketch
    └── my_script_badusb_arduino.ino      # Auto-generated
```

---

## 🎓 Educational Resources

### Learning DuckyScript
- [Official Rubber Ducky Wiki](https://github.com/hak5darren/USB-Rubber-Ducky/wiki)
- [DuckyScript Command Reference](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Duckyscript)

### Arduino Programming
- [Arduino Language Reference](https://www.arduino.cc/reference/en/)
- [Keyboard Library Documentation](https://www.arduino.cc/reference/en/language/functions/usb/keyboard/)

### DigiSpark Development
- [DigiSpark Wiki](http://digistump.com/wiki/digispark)
- [DigiKeyboard Library](http://digistump.com/wiki/digispark/tutorials/connecting)

---

## 🤝 Integration with Pure Pics

The BadUSB converter integrates seamlessly with Pure Pics workflow:

1. **Create payloads** in Pure Pics Rubber Ducky editor
2. **Embed in images** using steganography (optional)
3. **Auto-convert** DuckyScript to BadUSB using monitoring tool
4. **Deploy on hardware** for automatic execution

This creates a complete CPR (Create, Process, Run) pipeline from payload generation to hardware deployment.

---

**⚠️ Remember: This is for educational and authorized testing purposes only. Always obtain proper authorization before testing on any systems you don't own.**