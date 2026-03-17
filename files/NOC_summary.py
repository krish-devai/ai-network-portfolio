output = """
Router#show bgp summary
Neighbor        V    AS MsgRcvd MsgSent TblVer InQ OutQ Up/Down State/PfxRcd
10.10.10.1      4  65001    120    118      0   0    0  2d03h    25
10.10.10.2      4  65002      0      0      0   0    0  00:00:23 Active

Router#show processes cpu
CPU utilization for five seconds: 85%/70%; one minute: 72%; five minutes: 65%

Router#show interface status
GigabitEthernet0/1 is up, line protocol is up
  5 input errors, 3 CRC, 0 frame
GigabitEthernet0/2 is down, line protocol is down
  0 input errors, 0 CRC
GigabitEthernet0/3 is up, line protocol is up
  0 input errors, 4 CRC
"""

lines = output.splitlines()
last_interface = ""

bgp_issues = 0
interface_down = 0
crc_issues = 0
cpu_issue = False

print("Network Health Report")
print("---------------------")

for line in lines:
    if "GigabitEthernet" in line:
        last_interface = line.split()[0]

        if "line protocol is down" in line:
            interface_down += 1
            print("⚠️ Interface down:", last_interface)

    if "Active" in line:
        parts = line.split()
        neighbor_ip = parts[0]
        neighbor_asn = parts[2]
        neighbor_state = parts[9]

        bgp_issues += 1
        print("⚠️ BGP neighbor issue:", "IP:", neighbor_ip, "ASN:", neighbor_asn, "STATE:", neighbor_state)

    if "CPU utilization" in line:
        cpu_value = line.split(":")[1].split("%")[0].strip()

        if int(cpu_value) > 80:
            cpu_issue = True
            print("⚠️ High CPU:", cpu_value + "%")
        else:
            print("✅ CPU normal:", cpu_value + "%")

    if "CRC" in line:
        crc_value = line.split("CRC")[0].split()[-1]

        if int(crc_value) > 0:
            crc_issues += 1
            print("⚠️ CRC errors on", last_interface + ":", crc_value)

print("---------------------")
print("Summary")
print("BGP Issues:", bgp_issues)
print("Interface down:", interface_down)
print("CRC Issues:", crc_issues)
print("CPU Issue:", cpu_issue)

total_issues = bgp_issues + interface_down + crc_issues

if cpu_issue:
    total_issues += 1

if total_issues == 0:
    print("Overall Status: HEALTHY")
else:
    print("Overall Status: UNHEALTHY")
    print("Total Issues Found:", total_issues)
