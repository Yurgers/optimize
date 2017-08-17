# encoding: utf-8


# import codecs
import datetime
import re
import time
import iptools

# start = time.time()

param = [b'OS Assets\n',
         b'Show Configuration\n',
         b'env\n',
         b'uptime\n',
         b'date\n',
         b'hostname\n',
         b'uname -a\n',
         b'Enabled blades\n',
         b'vmstat 1 10\n',
         b'FireWall-1 Version Information\n',
         b'Free Memory Information - free -k -t\n',
         b'df -k\n',
         b'CP Status - OS (/opt/CPshrd-R77/bin/cpstat -f sensors os)\n',
         b'smartctl --all /dev/sda\n',
         b'raid_diagnostic\n',
         b'fw getifs\n',
         b'netstat -i\n',
         b'Interrupts Information (/proc/interrupts)\n',
         b'Cluster state\n',
         b'fw ctl multik stat\n',
         b'fw affinity -l -a -v\n',
         b'FW-1 Accelerator status\n',
         b'fwaccel stats -s\n',
         b'FireWall-1 Statistics (fw ctl pstat)\n',
         b'FireWall-1 Debug (fw ctl debug)\n',
         b'CP License\n',
         b'CPWD (Watch Dog) informaton\n',
         b'/opt/CPsuite-R77/fw1/boot/modules/fwkern.conf\n',
         b'smt status\n',
         b'IPS Status\n',
         b'SIM Affinity\n',
         b'CP Status - VPN (/opt/CPshrd-R77/bin/cpstat -f IKE vpn)\n',
         b'CP Status - VPN (/opt/CPshrd-R77/bin/cpstat -f ipsec vpn)\n',
         b'Traditional Overlapping Encryption Domains\n',
         b'Communities Overlapping Encryption Domains\n',
         b'Overlapping Encryption Domains\n',
         b'CP Status - IDENTITYSERVER (/opt/CPshrd-R77/bin/cpstat -f default identityServer)\n',
         b'CP Status - ANTIMALWARE (/opt/CPshrd-R77/bin/cpstat -f default antimalware)\n',
         b'CP Status - URLF (/opt/CPshrd-R77/bin/cpstat -f update_status urlf)\n',
         b'CP Status - APPI (/opt/CPshrd-R77/bin/cpstat -f update_status appi)\n',
         b'/opt/CPsuite-R77/fw1/conf/rad_services.C\n',
         b'/opt/CPsuite-R77/fw1/conf/anti_malware_rulebase.C\n',
         b'FireWall-1 Status - Anti Malware\n',
         b'netstat -i \n',
         b'High Availability interfaces (cphaprob -a if)\n',
         b'High Availability State (cphaprob state)\n',
         b'High Availability List (cphaprob -l list)\n',
         b'CPmonitor - traffic analysis\n',
         b'/opt/CPsuite-R77/fw1/boot/ha_boot.conf\n',
         b'Hotfix versions\n',
         b'/opt/CPsuite-R77/fw1/conf/fwaffinity.conf\n',
         b'FW-1 Accelerator statistics\n',
         # b'/opt/CPsuite-R77/fw1/database/dlp_net_objects.C\n',
         # b'/opt/CPsuite-R77/fw1/database/full_ips_objects.C\n',
         b'/opt/CPsuite-R77/fw1/database/myself_objects.C\n',
         # b'/opt/CPsuite-R77/fw1/database/netobj_objects.C\n',
         # b'/opt/CPsuite-R76/fw1/database/dlp_net_objects.C\n',
         # b'/opt/CPsuite-R76/fw1/database/full_ips_objects.C\n',
         b'/opt/CPsuite-R76/fw1/database/myself_objects.C\n',
         b'/opt/CPsuite-R77/fw1/database/slim_rules.C\n',
         b'/opt/CPsuite-R76/fw1/database/slim_rules.C\n',
         # b'/opt/CPsuite-R76/fw1/database/netobj_objects.C\n',
         b'/opt/CPsuite-R77/fw1/database/communities_objects.C\n',
         b'/opt/CPsuite-R76/fw1/database/communities_objects.C\n',
         b'/opt/CPsuite-R77/fw1/conf/Standard.pf\n',
         b'FireWall-1 Status\n'
         # b'/proc/net/bonding/bond'
         # b'/proc/net/bonding/bond0\n',
         # b'/proc/net/bonding/bond1\n',
         # b'/proc/net/bonding/bond2\n',
         # b'/proc/net/bonding/bond3\n'
         ]

start_end_section = (b'------------------------\n',
                     b'-----------------------\n',
                     b'----------------------\n',
                     b'==============================================\n',
                     b'------------------------------------------------------------------\n'
                     )

mes = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}

cpinfo_file = 'cpinfo.txt'
selekt = 'selekt.txt'
report = 'report.txt'
diagnostic = 'diagnostic.txt'

razdelit_for_sample = b'==============================================\n'


def selekt_razdel_by_text(file_ser, text):
    a = False
    b = True
    c = False
    razdel = []

    with open(file_ser, 'rb') as file:
        for line in file:
            if (line == razdelit_for_sample) and not a and b:
                # print(line)
                a = True
                b = True
                c = False

            elif a and (line == text):
                # print(line)
                a = True
                b = False
                c = False


            elif not b and (line == razdelit_for_sample):
                # print(line)

                a = False
                b = True
                c = True
            elif b and (line == razdelit_for_sample):
                # print(line)
                a = False
                b = True
                c = False

            elif c:
                if line == b'\n' or line == b' \n':
                    continue
                else:
                    razdel.append(line)

                    # if file_ser == 'diagnostic.txt':
                    # 	print(line)

    # print('\n'.join(razdel))
    return razdel


def selekt_text(text):
    razdel = selekt_razdel_by_text(selekt, text)
    # print(len(razdel))
    if len(razdel) < 1:  # если раздела нет в cpinfo идем в мой файл, но проверяем, чтобы совпадал hostname
        hostname_d = selekt_razdel_by_text(diagnostic, b'hostname\n')[0].decode('utf-8')
        if hostname_r == hostname_d:
            razdel = selekt_razdel_by_text(diagnostic, text)
            # else:
            # 	print('no diagnostic file')

    return razdel


def print_razdel_to_report(name_print, name_razdel):  # добавляем раздел полностью в файл репорта.
    razdel_to_report = selekt_text(name_razdel)
    if len(razdel_to_report) > 0:
        report_file.write(b'\n')
        report_file.write(name_print)
        for x in razdel_to_report:
            report_file.write(b'\t' + x)

    else:
        print('\n' + name_print.replace(b'\n', b'').decode('utf-8'))
        print('\tNO Data Files!!!')

    return razdel_to_report


# добавление к выборке
def add_selekt_file(add_rezdel):
    a = False
    b = True
    c = False
    selekt_file = open(selekt, 'ab')
    with open(cpinfo_file, 'rb') as file:
        for line in file:
            # print(i)

            if (line in start_end_section) and not a and b:
                a = True
                b = True
                c = False
            # razdelit_for_sample = line
            # print('1!!!' + line )

            elif a and (line in add_rezdel):
                # print('------------------------')
                selekt_file.write(b'\n' + razdelit_for_sample)
                # print(line)
                selekt_file.write(line)
                a = True
                b = False
                c = False

            elif not b and (line in start_end_section):
                # print(line)
                selekt_file.write(razdelit_for_sample + b'\n')
                a = False
                b = True
                c = True

            elif b and (line in start_end_section):
                a = False
                b = True
                c = False

            elif c:
                if (line == b'\n') or (b'Issuing' in line) or (b'lock database override' in line):
                    # print(i)
                    continue
                else:
                    # print(line)
                    selekt_file.write(line)
                    # print(line)
                    # time.sleep(1)

    selekt_file.close()


# если есть влан - нет ethtool -S  на основной интерфейс
def determination_interface(interf):
    interface_list = selekt_text(b'fw getifs\n')
    interface = interf
    if interface_list:
        for y in interface_list:
            if interf in y:
                interface = y.split()[1]
                break

    return interface


# --------------- выборка из cpinfo --------------------

def sample_from_cpinfo(cpinfo_file, selekt):
    ethtool_statistics = b'ethtool -S'
    ethtool_ring = b'ethtool -g'
    bond_settings = b'/proc/net/bonding/bond'

    database_objects_C = [
        b'/opt/CPsuite-R77/fw1/database/full_ips_objects.C\n',
        b'/opt/CPsuite-R77/fw1/database/netobj_objects.C\n',
        b'/opt/CPsuite-R76/fw1/database/full_ips_objects.C\n',
        b'/opt/CPsuite-R76/fw1/database/netobj_objects.C\n'
    ]

    Cluster = False
    selekt_host = False
    full_ips_objects = False
    selekt_host_name_2 = False
    sd_update = False
    Standard_pf = False
    Standard_pf_table = False
    a = False
    b = True
    c = False
    i = 0

    # file = codecs.open(cpinfo_file, b'r', b'utf-8')
    #  codecs.open(cpinfo_file, encoding='utf_8_sig', mode='r')

    # составление выборки
    selekt_file = open(selekt, 'wb')
    with open(cpinfo_file, 'rb') as file:
        for line in file:
            i = i + 1  # для отладки, чтобы узнать на какой строке в файле ошибка.

            line = line.replace(b'\r', b'')  # в последних версиях cpinfo появились перевод строк

            if (line in start_end_section) and (not a) and b:  # находим начало секции
                a = True
                b = True
                c = False
            # razdelit_for_sample = line
            # print('1!!!' + line )

            elif (a and
                      (line in param or
                           (bond_settings in line) or  # line[:-2] in bond_settings or line[:-3] in bond_settings or     #отбираем bondX и bondXX
                           (ethtool_statistics in line) or
                           (ethtool_ring in line)
                      )):
                # len(re.findall(ethtool_statistics, line)) > 0  or  len(re.findall( ethtool_ring, line)) > 0 )
                # print('------------------------')

                full_ips_objects = False
                database_rules = False

                if line in b'hostname\n':
                    selekt_host = True

                if line in database_objects_C:
                    full_ips_objects = True
                # print(line)
                else:
                    full_ips_objects = False

                if line == b'/opt/CPsuite-R77/fw1/database/slim_rules.C\n':
                    database_rules = True

                if line == b'/opt/CPsuite-R77/fw1/conf/Standard.pf\n':
                    Standard_pf = True
                # if Standard_pf:
                # 	print (line)

                else:
                    Standard_pf = False

                selekt_file.write(b'\n' + razdelit_for_sample)
                # print(line)
                selekt_file.write(line)
                a = True
                b = False
                c = False

            elif not b and (line in start_end_section):
                # print(line)
                selekt_file.write(razdelit_for_sample + b'\n')

                a = False
                b = True
                c = True

            elif b and (line in start_end_section):
                a = False
                b = True
                c = False


            elif c:
                if (b'Issuing' in line) or (line == b'\n') or (b'lock database override' in line):
                    # print(i)
                    continue

                elif database_rules:  # чистим slim_rules.C
                    if b'sd_update_version' in line:
                        selekt_file.write(line)
                        sd_update = True
                        sd_update_1 = 1

                elif sd_update:
                        # print(line)
                        selekt_file.write(line)
                        sd_update_1 += 1
                        if sd_update_1 == 8:
                            sd_update = False

                else:
                    # print(line)
                    if selekt_host:  # Убераем лишний лог!!!
                        selekt_host_name = line
                        # selekt_host_name = b" (" + selekt_host_name
                        # print (selekt_host_name)
                        selekt_host = False

                    if full_ips_objects:
                        # print(line)
                        if (len(line.split(b':')) == 2) and (len(line.split(b':')[1]) > int(len(selekt_host_name) / 2)):
                            # print (line.split(b':')[1])
                            if line.split(b':')[1].replace(b'\n', b'').replace(b' ', b'').replace(b'(',
                                                                                                  b'') in selekt_host_name:
                                # print (line.split(b':')[1].replace(b'\n', b'').replace(b' ', b'').replace(b'(', b''))
                                # print (line)
                                otstup = line.split(b':')[0] + b')\n'
                                # print(otstup)
                                selekt_host_name_2 = True
                                selekt_file.write(line)

                            elif selekt_host_name_2:
                                selekt_file.write(line)


                        # elif selekt_host_name_2 and (otstup == line) :
                        # 	selekt_file.write(line)
                        # 	selekt_host_name_2 = False
                        elif selekt_host_name_2:
                            selekt_file.write(line)
                            if (otstup == line):
                                selekt_host_name_2 = False

                    if Standard_pf:  # ВЫборка о VPN
                        # print (line)
                        if b'VPN methods table' in line:
                            # print('print')

                            Standard_pf_table = True
                        # selekt_file.write(line)

                        elif b'VPN Routing table' in line:
                            Standard_pf_table = True

                        if Standard_pf_table:
                            # print('print')
                            selekt_file.write(line)

                            if b'};' in line:
                                # print(line)
                                Standard_pf_table = False

                    else:
                        selekt_file.write(line)

            elif line == b'Cluster state -----------------------\n':
                Cluster = True
                selekt_file.write(razdelit_for_sample)
                selekt_file.write(b'Cluster state\n')
                selekt_file.write(razdelit_for_sample)

            elif line == b'Routes -----------------------\n':
                Cluster = False

            elif Cluster:
                # print(line)
                selekt_file.write(line)
                # print(line)

    selekt_file.close()


def generation_file_report():
    # --------------- построение отчета --------------------
    # --------------- построение отчета --------------------
    # --------------- построение отчета --------------------
    razdel_to_report = selekt_text(b'hostname\n')
    # print(razdel_to_report)
    global hostname_r
    hostname_r = razdel_to_report[0].replace(b'\n', b'').decode('utf-8')
    print('\nhostname: ' + hostname_r)

    for x in razdel_to_report:
        report_file.write(b'Analiz perfomance:\t' + x)

    # ц└ц═ц╡ц═ ц╠цґц©ц╡ц╗ц© CPInfo
    print_razdel_to_report(b'\ndata techdump:\n', b'date\n')

    # информация об устройстве.
    razdel_to_report = selekt_text(b'OS Assets\n')
    if razdel_to_report:
        razdel_to_report = print_razdel_to_report(b'Obshhaja informacija ob ustrojstve:\n', b'OS Assets\n')
        for x in razdel_to_report:
            if re.findall(br'^Model:', x):
                print(x.replace(b'\n', b'').decode('utf-8'))

    else:  # Для вывода версии 41k
        razdel_to_report = selekt_text(b'env\n')
        if razdel_to_report:
            for x in razdel_to_report:
                if re.findall(b'ASG_PRODUCT', x):
                    print(x.replace(b'\n', b'').decode('utf-8'))

    # Версия Check Point:
    razdel_to_report = print_razdel_to_report(b'Version Check Point:\n', b'FireWall-1 Version Information\n')
    if razdel_to_report:
        for x in razdel_to_report:
            if b'kernel:' in x:
                print(x.replace(b'\n', b'').decode('utf-8'))

    # Uptime system:
    razdel_to_report = print_razdel_to_report(b'Uptime system:\n', b'uptime\n')

    print('\nUptime system:')

    x = (re.findall(br'(\d*) days', razdel_to_report[0]))

    if len(x) == 0:
        x = [b'0']

    if int(x[0]) < 7:
        print('\t' + str(x[0].decode('utf-8')) + ' days - small uptime!!!')
    else:
        print('\t' + x[0].decode('utf-8') + ' days - OK')

    # Разрядность системы
    print_razdel_to_report(b'uname -a:\n', b'uname -a\n')

    # Количество просессоров
    razdel_to_report = selekt_text(b'count CPUs\n')
    report_file.write(b'\nCount CPUs:\n')
    print('\nCount CPUs:')
    CPUs = 0
    if razdel_to_report:
        for x in razdel_to_report:
            # print('\t'+x.replace(b'\n', b'').decode('utf-8'))
            # report_file.write(b'\t'+x.replace(b'\n', b''))
            CPUs = int(x.decode('utf-8').split(':')[1])

    if CPUs == 0:
        razdel_to_report = selekt_text(b'Interrupts Information (/proc/interrupts)\n')
        for x in razdel_to_report:
            if re.findall(br'CPU\d+', x):
                CPUs = len(re.findall(r'CPU(\d+)', x.decode('utf-8')))

    report_file.write(b'\tCPUs Number:\t' + bytes(str(CPUs), 'ascii') + b'\n')
    print('\tCPUs Number:\t' + str(CPUs))

    # Hyperspect
    print_razdel_to_report(b'Hyperspect enabled?:\n', b'smt status\n')

    # включенные blades
    report_file.write(b'\n')
    report_file.write(b'Enabled blades:\n')
    razdel_to_report = selekt_text(b'Enabled blades\n')
    print('\nenabled_blades:')
    enabled_blades = ''
    if razdel_to_report:
        enabled_blades = razdel_to_report[0].decode('utf-8').split()
        razdel_to_report = razdel_to_report[0].split()
        a = 0
        for x in razdel_to_report:
            a = a + 1
            report_file.write(b'\t' + bytes(str(a), 'ascii') + b'. ' + x + b'\n')
            print('\t' + str(a) + '. ' + x.decode('utf-8'))
    else:
        print('\tNO Data Files!!!')

    # лицензии
    razdel_to_report = print_razdel_to_report(b'CP License:\n', b'CP License\n')
    if razdel_to_report:
        license_stat = True
        print('\nCP License:')
        for x in razdel_to_report:
            if re.findall(br'(\d{1,2}...\d{4})', x):
                data_license_raw = (re.findall(r'(\d{1,2}...\d{4})', x.decode('utf-8'))[0])
                data_license = datetime.date(int(data_license_raw[-4:]), mes[re.findall(r'\D+', data_license_raw)[0]],
                                             int(data_license_raw[:1]))
                delta = data_license - datetime.date.today()
                # print (int(str(delta).split()[0]))
                if (int(str(delta).split()[0])) < 30:
                    print(
                        '\t' + str(delta).split(',')[0] + '\t-\t' + x.replace(b'\n', b'').decode('utf-8').replace('|',
                                                                                                                  ''))
                    license_stat = False

            elif b'trial period' in x:
                print('\tTrial period ' + (re.findall(r'(\d+ days)', x.decode('utf-8'))[0]) + '!!!')
                license_stat = False

        if license_stat:
            print('\tOK')

    # ny_2011 = datetime.date(2011,7,1)
    # print( datetime.date.today())
    # print(ny_2011)
    # delta = ny_2011 - datetime.date.today()
    # print(delta)


    # установленные Hotfix versions
    print_razdel_to_report(b'Hotfix versions:\n', b'Hotfix versions\n')

    # ц┤ц═цёц╟цЁцїц╙ц═ ц╠ц╗ц╠ц╡ц╔ц╛ц╩
    print_razdel_to_report(b'vmstat:\n', b'vmstat 1 10\n')

    # история использования процессора
    razdel_to_report = selekt_text(b'sar CPU\n')

    if razdel_to_report:
        unilization_CPU = []

        unilization_CPU_0 = []
        unilization_CPU_1 = []
        unilization_CPU_2 = []
        unilization_CPU_3 = []
        unilization_CPU_4 = []
        unilization_CPU_5 = []
        unilization_CPU_60_min_fool = False
        unilization_CPU_30_min_fool = False

        data_unilization_CPU = []
        unilization_CPU_30_min = []
        data_unilization_CPU_30_min = []
        unilization_CPU_60_min = []
        data_unilization_CPU_60_min = []

        time_loop = -1
        print('\nsar CPU:')

        for x in razdel_to_report:

            if re.findall(br'(\d{2}/\d{2}/\d{2})', x):  # Дата
                data_sar = (re.findall(r'(\d{2}/\d{2}/\d{2})', x.decode('utf-8'))[0])
            # print ('\n' + data_sar)

            elif x.split()[1] == b'all':
                # print ( data_sar + ' : ' + x.split()[0].decode('utf-8') + ':' + x.split()[1].decode('utf-8') )
                unilization_CPU_5 = unilization_CPU_4[:]
                unilization_CPU_4 = unilization_CPU_3[:]
                unilization_CPU_3 = unilization_CPU_2[:]
                unilization_CPU_2 = unilization_CPU_1[:]
                unilization_CPU_1 = unilization_CPU_0[:]
                time_loop = time_loop + 1

            elif (re.findall(br'(\d{2}:\d{2}:\d{2})\s*\d+', x)):
                # print ('len(unilization_CPU) = ' + str(len(unilization_CPU)))
                # print (int(x.decode('utf-8').split()[1])+1)
                num_CPU = int(x.decode('utf-8').split()[1])  # номер CPU
                data_load_CPU = data_sar + '-' + x.decode('utf-8').split()[0]  # время снятия загрузки процессора
                load_CPU = float(x.decode('utf-8').split()[7])

                if len(unilization_CPU) < num_CPU + 1:
                    unilization_CPU.append(load_CPU)
                    data_unilization_CPU.append(data_load_CPU)
                    unilization_CPU_30_min.append(load_CPU)
                    data_unilization_CPU_30_min.append(data_load_CPU)
                    unilization_CPU_60_min.append(load_CPU)
                    data_unilization_CPU_60_min.append(data_load_CPU)

                    unilization_CPU_0 = unilization_CPU[:]

                unilization_CPU_0[num_CPU] = load_CPU

                if load_CPU < unilization_CPU[num_CPU]:
                    unilization_CPU[num_CPU] = load_CPU
                    data_unilization_CPU[num_CPU] = data_load_CPU

                if 0 < time_loop < 3:
                    unilization_CPU_30_min[num_CPU] = load_CPU + unilization_CPU_30_min[num_CPU]
                    data_unilization_CPU_30_min[num_CPU] = data_load_CPU

                    if time_loop == 2:
                        unilization_CPU_30_min_fool = True
                        # print ( unilization_CPU_30_min)

                if 0 < time_loop < 6:
                    unilization_CPU_60_min[num_CPU] = load_CPU + unilization_CPU_60_min[num_CPU]
                    data_unilization_CPU_60_min[num_CPU] = data_load_CPU

                    if time_loop == 5:
                        unilization_CPU_60_min_fool = True
                        # print ( unilization_CPU_60_min)

                        # print ("\n\n" +  str(time_loop) )
                        # print ( str(int(x.decode('utf-8').split()[1])) + '    :    ' +  str(float(x.decode('utf-8').split()[7])))
                        # print ("unilization_CPU_30_min = ")
                        # print ( unilization_CPU_30_min)
                        # # print (data_unilization_CPU)

                        # print ("unilization_CPU_60_min = " )
                        # print ( unilization_CPU_60_min)
                        # # print (data_unilization_CPU)

                if unilization_CPU_30_min_fool:
                    if unilization_CPU_30_min[num_CPU] > unilization_CPU_0[num_CPU] + unilization_CPU_1[num_CPU] + \
                        unilization_CPU_2[num_CPU]:
                        unilization_CPU_30_min[num_CPU] = unilization_CPU_0[num_CPU] + unilization_CPU_1[num_CPU] + \
                                                          unilization_CPU_2[num_CPU]
                        data_unilization_CPU_30_min[num_CPU] = data_load_CPU

                if unilization_CPU_60_min_fool:
                    if unilization_CPU_60_min[num_CPU] > unilization_CPU_0[num_CPU] + unilization_CPU_1[num_CPU] + \
                        unilization_CPU_2[num_CPU] + unilization_CPU_3[num_CPU] + unilization_CPU_4[num_CPU] + \
                        unilization_CPU_5[num_CPU]:
                        unilization_CPU_60_min[num_CPU] = unilization_CPU_0[num_CPU] + unilization_CPU_1[num_CPU] + \
                                                          unilization_CPU_2[num_CPU] + unilization_CPU_3[num_CPU] + \
                                                          unilization_CPU_4[num_CPU] + unilization_CPU_5[num_CPU]
                        data_unilization_CPU_60_min[num_CPU] = data_load_CPU


                        # if  len(re.findall( r'(\d{2}:\d{2}:\d{2})\s*3', x.decode('utf-8'))) > 0 :             #Графическое представление загрузки указанного процессора
                        #   a = 2                                                                   #Маштаб 1/а

                        #   b = x.decode('utf-8').split()[0]                                        #time
                        #   c =  int(float(x.decode('utf-8').split()[2] ) / a )                     #user
                        #   d =  int(float(x.decode('utf-8').split()[4] ) / a )                     #%system
                        #   e =  int(float(x.decode('utf-8').split()[7] ) / a )                     #%idle
                        #   f =  x.decode('utf-8').split()[7]                                       #%idle

                        #   print (b + '\t' + ('u' * c)  +  ('s' * d) +   ('*' * (e-d-c))  +  (' ' * (int (100 / a)  -e  )) + '\t'  +   f  )


                        # print (time_loop)
                        # print (unilization_CPU_0)
                        # print (unilization_CPU_1)
                        # print (unilization_CPU_2)
                        # print (unilization_CPU_3)
                        # print (unilization_CPU_4)
                        # print (unilization_CPU_5)

        # print ("\n\nFin\n\n")
        print("unilization_CPU = ")
        for uni in range(len(unilization_CPU)):
            print('CPU_' + str(uni) + ':\t' + "{0:.2f}".format(unilization_CPU[uni]) + '\t-\t' + str(
                data_unilization_CPU[uni]))

            "{0:.2f}".format(unilization_CPU[uni])

        print("\nunilization_CPU_30_min = ")
        for uni in range(len(unilization_CPU_30_min)):
            print('CPU_' + str(uni) + ':\t' + "{0:.2f}".format(unilization_CPU_30_min[uni] / 3) + '\t-\t' + str(
                data_unilization_CPU_30_min[uni]))

        print("\nunilization_CPU_60_min = ")
        for uni in range(len(unilization_CPU_60_min)):
            print('CPU_' + str(uni) + ':\t' + "{0:.2f}".format(unilization_CPU_60_min[uni] / 6) + '\t-\t' + str(
                data_unilization_CPU_60_min[uni]))

    # info o memory
    razdel_to_report = print_razdel_to_report(b'Memory Information:\n', b'Free Memory Information - free -k -t\n')

    if razdel_to_report:
        print('\nMemory Information:')
        for x in razdel_to_report:
            if x.decode('utf-8').split()[0] == 'Mem:':
                a = x.decode('utf-8').split()
                print('\tused ' + a[0] + '\t' + str(round((int(a[2]) / int(a[1]) * 100), 2)) + ' %')
                print('\tReal Free ' + a[0] + '\t' + str(round((int(a[2]) - int(a[5]) - int(a[6])), 2)) + ' byte')
                print('\tReal Free ' + a[0] + '\t' + str(
                    round((int(a[2]) - int(a[5]) - int(a[6])) / int(a[1]) * 100, 2)) + ' %')

            elif x.decode('utf-8').split()[0] == 'Swap:':
                print('\tused ' + x.decode('utf-8').split()[0] + '\t' + str(
                    round((int(x.decode('utf-8').split()[2]) / int(x.decode('utf-8').split()[1]) * 100), 2)) + ' %')

    # количество свободного места
    razdel_to_report = print_razdel_to_report(b'Free Dis:\n', b'df -k\n')

    if razdel_to_report:
        print('\nFree Disk:')
        disk_ok = True
        for x in razdel_to_report:
            a = (re.findall(r'(\d+)%', x.decode('utf-8')))
            if a:
                # print(int(a[0]))
                if int(a[0]) > 90:
                    print('\t' + (re.findall(r'% (.+)', x.decode('utf-8'))[0]) + ' used to ' + a[0] + '%')
                    disk_ok = False
        if disk_ok:
            print('\tOK')

        # показать большие файли при заполеном диске
        if not disk_ok:
            print_razdel_to_report(b'big file (<250M):\n', b'big file (<250M)\n')

    razdel_to_report = selekt_text(b'/opt/CPsuite-R77/fw1/database/myself_objects.C\n')
    if razdel_to_report:
        for x in razdel_to_report:
            if b':auto_calc_concurrent_conns (false)' in x:
                print('\nOptimizations:')
                print('\tLimit Connections: Manual mode   -   !!!!!')
            elif b':calculation_type (manual)' in x:
                print('\tCalculate connections hash table: Manual mode   -   !!!!!')

    # SMART
    razdel_to_report = print_razdel_to_report(b'SMART:\n', b'smartctl --all /dev/sda\n')

    if razdel_to_report:
        print('\nSMART:')
        for x in razdel_to_report:
            a = (re.findall(r'(SMART Health Status: .+)', x.decode('utf-8')))
            if len(a) > 0:
                print('\t' + a[0])

    # ip adress активных интерфейсов
    razdel_to_report = selekt_text(b'fw getifs\n')
    if razdel_to_report:
        objects_C = selekt_text(b'/opt/CPsuite-R77/fw1/database/myself_objects.C\n')
        # print (len(objects_C))
        # print ('/opt/CPsuite-R76/fw1/database/netobj_objects.C')
        if len(objects_C) == 0:
            objects_C = selekt_text(b'/opt/CPsuite-R77/fw1/database/full_ips_objects.C\n')
            # print (len(objects_C))
            # print ('/opt/CPsuite-R77/fw1/database/dlp_net_objects.C')
            if len(objects_C) == 0:
                objects_C = selekt_text(b'/opt/CPsuite-R77/fw1/database/dlp_net_objects.C\n')
                # print (len(objects_C))
                # print ('/opt/CPsuite-R77/fw1/database/dlp_net_objects.C')
                if len(objects_C) == 0:
                    objects_C = selekt_text(b'/opt/CPsuite-R77/fw1/database/netobj_objects.C\n')
                    # print (len(objects_C))
                    # print ('/opt/CPsuite-R76/fw1/database/myself_objects.C\n')

                    if len(objects_C) == 0:
                        objects_C = selekt_text(b'/opt/CPsuite-R76/fw1/database/myself_objects.C\n')
                        if len(objects_C) == 0:
                            objects_C = selekt_text(b'/opt/CPsuite-R76/fw1/database/full_ips_objects.C\n')

        # print     ('objects_C' )
        # print   (objects_C)


        # print(razdel_to_report)
        interfaces_start_t = False
        ipaddr_t = False
        hostname_r_true = True
        xx = -1
        for x in razdel_to_report:
            xx = xx + 1
            refname = b''
            for y in objects_C:

                if hostname_r_true and re.findall(rb': \((.+)', y):
                    hostname_r = (re.findall(r': \((.+)', y.decode('utf-8')))[0]
                    # print(hostname_r)
                    hostname_r_true = False

                if len(y.split(b':')) > 1:

                    if y.split(b':')[1] == b'interfaces (\n':  # находим где начинается описание интерфейсов
                        interfaces_start = (y.split(b':')[0])
                        interfaces_start_t = True
                        # print("interfaces_start")
                        # print(y)

                if interfaces_start_t:  # находим где заканчивается описание интерфейсов
                    if (y == interfaces_start + b')\n'):
                        # print("interfaces_stop")
                        # print(y)
                        interfaces_start_t = False

                    elif b'ipaddr' in y:
                        # print(x.split()[2])
                        # print(y)
                        if x.split()[2] == ((re.findall(rb'\((.+)\)', y))[0]):  # находим интересеющий насс интерфейс
                            ipaddr_t = True
                        # print(x.split()[2])
                        # print((re.findall( rb'\((.+)\)', y))[0])
                        # print(y)
                        # print(x)
                        else:
                            ipaddr_t = False


                    elif ipaddr_t and b':dmz' in y:
                        # print(y)
                        if (re.findall(rb'\((.+)\)', y))[0] == b'false':  # No DMZ
                            leads_to_DMZ = False

                        elif (re.findall(rb'\((.+)\)', y))[0] == b'true':  # DMZ
                            leads_to_DMZ = True

                            # razdel_to_report[xx] = x[:-1] + b' - ' +  leads_to_DMZ + x[-1:]
                            # print (xx)
                            # print (leads_to_DMZ)
                            # print (razdel_to_report[xx])


                    elif ipaddr_t and b':leads_to_internet' in y:
                        # print(x)
                        # print(y)
                        # print((re.findall( rb'\((.+)\)', y))[0])
                        if (re.findall(rb'\((.+)\)', y))[0] == b'true':
                            leads_to_internet = b'External'
                            access = b''
                        else:
                            if leads_to_DMZ:
                                leads_to_internet = b'DMZ'
                            else:
                                leads_to_internet = b'Internal'

                                # print(leads_to_internet)
                                # print(razdel_to_report)
                                # print(razdel_to_report.index(x))


                                # break
                                # print(razdel_to_report)

                    elif ipaddr_t and b':access' in y:
                        if (re.findall(rb'\((.+)\)', y))[0] == b'this':
                            access = b' - Defined'

                        elif (re.findall(rb'\((.+)\)', y))[0] == b'undefined':
                            access = b' - Not Defined'

                        elif (re.findall(rb'\((.+)\)', y))[0] == b'specific':
                            access = b' - Specific'


                    elif ipaddr_t and b':refname' in y:
                        if access == b' - Specific':
                            access = access + b' ' + (re.findall(rb'(\(.+\))', y))[0]
                        else:
                            refname = b' - Don`t chack packets from: ' + (re.findall(rb'(\(.+\))', y))[0]


                    elif ipaddr_t and b':perform_anti_spoofing' in y:
                        if (re.findall(rb'\((.+)\)', y))[0] == b'false':
                            anti_spoofing = b' - Anti Spoofing: OFF !!!'
                        elif (re.findall(rb'\((.+)\)', y))[0] == b'true':
                            anti_spoofing = b' - Anti Spoofing: ' + monitor_anti_spoofing + Log


                    elif ipaddr_t and b':log' in y:
                        Log = b' - Log: ' + (re.findall(rb'\((.+)\)', y))[0]


                    elif ipaddr_t and b':monitor_anti_spoofing' in y:
                        if (re.findall(rb'\((.+)\)', y))[0] == b'true':
                            monitor_anti_spoofing = refname + b'Detect'
                        elif (re.findall(rb'\((.+)\)', y))[0] == b'false':
                            monitor_anti_spoofing = refname + b'Prinvent'

            razdel_to_report[xx] = razdel_to_report[xx][:-1] + b' - ' + leads_to_internet + access + anti_spoofing + \
                                   razdel_to_report[xx][-1:]

        # elif b':netmask (' + x.split()[3] in y :
        #   print(y)

        print('\ninterface:')
        report_file.write(b'\ninterface:\n')
        for x in razdel_to_report:
            print('\t' + x.replace(b'\n', b'').decode('utf-8'))
            report_file.write(b'\t' + x)

        razdel_to_report = selekt_text(b'/opt/CPsuite-R77/fw1/database/myself_objects.C\n')
        if len(razdel_to_report) > 1:
            ISP_Redundancy = ['']
            misp_isps = False
            for y in razdel_to_report:
                if b':misp_active' in y:
                    if b'true' in y:
                        print('\nISP Redundancy:\tActive')
                    elif b'false' in y:
                        print('\nISP Redundancy:\tNO Active')
                        break

                if b':misp_load_sharing' in y:
                    if b'false' in y:
                        ISP_Redundancy[0] = 'Mode:\tPrimary/Backup'
                    else:
                        ISP_Redundancy[0] = 'Mode:\tLoad Sharing'

                elif b':misp_isps' in y:
                    misp_isps = True

                elif misp_isps and re.findall(br':\d \(', y):
                    z = int((re.findall(r':(\d) \(', y.decode('utf-8')))[0]) + 1
                    ISP_Redundancy.append('')
                # elif misp_isps and b':1 (' in y :
                #   z = 2

                elif misp_isps and b':misp_interface' in y:
                    ISP_Redundancy[z] = (re.findall(r'\((.+)\)', y.decode('utf-8')))[0]

                elif misp_isps and b':misp_nexthop' in y:
                    ISP_Redundancy[z] = ISP_Redundancy[z] + '\tnexthop: ' + \
                                        (re.findall(r'\((.+)\)', y.decode('utf-8')))[0]

                elif misp_isps and b':misp_primary_isp' in y:
                    if b'true' in y:
                        ISP_Redundancy[z] = ISP_Redundancy[z] + '\t   -\tPrimary'
                    else:
                        ISP_Redundancy[z] = ISP_Redundancy[z] + '\t   -\tBackup'

            for y in ISP_Redundancy:
                print('\t' + y)

    # какие интерфейсы находятся в бонде
    for i in range(50):
        razdel_to_report = selekt_text(b'/proc/net/bonding/bond' + bytes(str(i), 'ascii') + b'\n')
        if razdel_to_report:
            report_file.write(b'\nbond' + bytes(str(i), 'ascii') + b':\n')
            print('\nbond' + str(i) + ':')
            for x in razdel_to_report:
                if b'Interface' in x:
                    Interface = b'\t' + x.split(b':')[1].replace(b' ', b'')
                    print(Interface.replace(b'\n', b'').decode('utf-8'))
                    report_file.write(Interface)

    # Kernel Interface table
    razdel_to_report = print_razdel_to_report(b'netstat -i:\n', b'netstat -i \n')
    Total_pkts = 1
    if razdel_to_report:
        print('\nnetstat -i:')
        interrupts_t = False
        for x in razdel_to_report:
            RX_DRP = True
            TX_DRP = True
            RX_OVR = True
            TX_OVR = True
            RX_ERR = True
            TX_ERR = True
            if len(x.split()) == 12:
                if x.decode('utf-8').split()[0] != 'Iface':

                    if b'bond' not in x:
                        Total_pkts = Total_pkts + int(x.decode('utf-8').split()[3])
                    # print (Total_pkts)

                    if x.decode('utf-8').split()[3] != '0':
                        if (int(x.decode('utf-8').split()[4]) * 100 / int(x.decode('utf-8').split()[3])) > 0.001:
                            print('\t' + x.decode('utf-8').split()[0] + '\t-\tRX-ERR  Error !!!!\t' + str(
                                round(int(x.decode('utf-8').split()[4]) * 100 / int(x.decode('utf-8').split()[3])), 3))
                            print('\t\t' + 'Проверьте кабель!!!')
                            RX_ERR = False

                            # Добовляем данные об ошибках
                            # add_selekt_file(b'ethtool -S ' + x.split()[0] + b'\n')
                            interface = determination_interface(x.split()[0])
                            ethtool_s = selekt_text(b'ethtool -S ' + interface + b'\n')

                            if ethtool_s:
                                print('\t\terrors to interface:')
                                report_file.write(b'\n')
                                report_file.write(b'ethtool -S ' + interface + b':\n')
                                for y in ethtool_s:
                                    if b'rx_errors' in y:
                                        print('\t\t' + y.replace(b'\n', b'').decode('utf-8'))
                                        report_file.write(b'\t' + y)
                                    elif b'rx_length_errors' in y:
                                        print('\t\t' + y.replace(b'\n', b'').decode('utf-8'))
                                        report_file.write(b'\t' + y)
                                    elif b'rx_crc_errors' in y:
                                        print('\t\t' + y.replace(b'\n', b'').decode('utf-8'))
                                        report_file.write(b'\t' + y)
                                    elif b'rx_frame_errors' in y:
                                        print('\t\t' + y.replace(b'\n', b'').decode('utf-8'))
                                        report_file.write(b'\t' + y)
                                    elif b'rx_align_errors' in y:
                                        print('\t\t' + y.replace(b'\n', b'').decode('utf-8'))
                                        report_file.write(b'\t' + y)
                                    elif y == b'no stats available\n':
                                        print('\t\t\t' + y.replace(b'\n', b'').decode('utf-8'))
                                        report_file.write(b'\t' + y)

                            else:
                                print('\t\tнет данных об errors:')

                        if (int(x.decode('utf-8').split()[5]) * 100 / int(x.decode('utf-8').split()[
                                                                              3])) > 0.01:  # в отличии от других необезательно должен быть равен 0
                            print('\t' + x.decode('utf-8').split()[0] + '\t-\tRX-DRP  Error !!!!')
                            RX_DRP = False
                            interrupts_t = True

                            # Добовляем данные об ошибках
                            # if RX_ERR:
                            # add_selekt_file(b'ethtool -S ' + x.split()[0] + b'\n')
                            interface = determination_interface(x.split()[0])

                            ethtool_s = selekt_text(b'ethtool -S ' + interface + b'\n')
                            if ethtool_s:
                                print('\t\terrors to interface:')
                                report_file.write(b'\n')
                                report_file.write(b'ethtool -S ' + interface + b':\n')
                                for y in ethtool_s:
                                    if b'x_missed_errors' in y:
                                        print('\t\t' + y.replace(b'\n', b'').decode('utf-8'))
                                        report_file.write(b'\t' + y)
                                    elif b'rx_fifo_errors' in y:
                                        print('\t\t' + y.replace(b'\n', b'').decode('utf-8'))
                                        report_file.write(b'\t' + y)
                                    elif b'rx_over_errors' in y:
                                        print('\t\t' + y.replace(b'\n', b'').decode('utf-8'))
                                        report_file.write(b'\t' + y)
                                    elif b'rx_length_errors' in y:
                                        print('\t\t' + y.replace(b'\n', b'').decode('utf-8'))
                                        report_file.write(b'\t' + y)
                                    elif b'rx_long_length_errors' in y:
                                        print('\t\t' + y.replace(b'\n', b'').decode('utf-8'))
                                        report_file.write(b'\t' + y)
                                    elif b'rx_short_length_errors' in y:
                                        print('\t\t' + y.replace(b'\n', b'').decode('utf-8'))
                                        report_file.write(b'\t' + y)
                                    elif y == b'no stats available\n':
                                        print('\t\t\t' + y.replace(b'\n', b'').decode('utf-8'))
                                        report_file.write(b'\t' + y)
                            else:
                                print('\t\tнет данных об errors:')

                        if (int(x.decode('utf-8').split()[6]) * 100 / int(x.decode('utf-8').split()[3])) > 0.001:
                            print('\t' + x.decode('utf-8').split()[0] + '\t-\tRX-OVR  Error !!!!\t' + str(
                                round(int(x.decode('utf-8').split()[6]) * 100 / int(x.decode('utf-8').split()[3]),
                                      3)) + '%')
                            print('\t\t' + 'уменишите скорость на данном интерфейсе или создайте bond')

                            # Добовляем данные о flow control
                            # if RX_ERR and RX_DRP:
                            # add_selekt_file(b'ethtool -S ' + x.split()[0] + b'\n')


                            interface = determination_interface(x.split()[0])

                            ethtool_s = selekt_text(b'ethtool -S ' + interface + b'\n')
                            print('\t\tиспользование flow control:')
                            report_file.write(b'\n')
                            report_file.write(b'ethtool -S ' + interface + b':\n')
                            if ethtool_s:
                                for y in ethtool_s:
                                    if b'flow_control' in y:
                                        print('\t\t' + y.replace(b'\n', b'').decode('utf-8'))
                                        report_file.write(b'\t' + y)
                            else:
                                print('\t\tнет данных flow control:')
                                report_file.write(b'\tno data flow control\n')

                            RX_OVR = False

                            print('')

                    if x.decode('utf-8').split()[7] != '0':
                        if (int(x.decode('utf-8').split()[8]) * 100 / int(x.decode('utf-8').split()[7])) > 0.001:
                            print('\t' + x.decode('utf-8').split()[0] + '\t-\tTX-ERR  Error !!!!')
                            TX_ERR = False
                        if (int(x.decode('utf-8').split()[9]) * 100 / int(x.decode('utf-8').split()[7])) > 0.01:
                            print('\t' + x.decode('utf-8').split()[0] + '\t-\tTX-DRP  Error !!!!')
                            TX_DRP = False
                        if (int(x.decode('utf-8').split()[10]) * 100 / int(x.decode('utf-8').split()[7])) > 0.001:
                            print('\t' + x.decode('utf-8').split()[0] + '\t-\tTX-OVR  Error !!!!')
                            TX_OVR = False

                    if RX_DRP and TX_DRP and RX_OVR and TX_OVR and RX_ERR and TX_ERR:
                        if len(x.decode('utf-8').split()[0]) < 8:
                            print('\t' + x.decode('utf-8').split()[0] + '\t\t-\tOK')
                        else:
                            print('\t' + x.decode('utf-8').split()[0] + '\t-\tOK')

                    if not (len(re.findall(b'bond', x.split()[0])) > 0):  # у bond нет буфера :)
                        # add_selekt_file(b'ethtool -g ' + x.split()[0] + b'\n')                                        #проверяем размер буффера кольца, польшой размер не всегда хорошо.
                        RX_buff = print_razdel_to_report(b'ethtool -g ' + x.split()[0] + b':\n',
                                                         b'ethtool -g ' + x.split()[0] + b'\n')
                        if len(RX_buff) > 1:
                            settings = False
                            for y in RX_buff:
                                if y == b'Current hardware settings:\n':
                                    # print('\t\t' + y.replace(b'\n', b'').decode('utf-8'))
                                    settings = True
                                elif settings:

                                    if int(y.decode('utf-8').split(':')[1]) > 2048:
                                        print(
                                            '\t\t\t' + y.replace(b'\n', b'').decode('utf-8') + '\t-\tBufferBloat!!!!!')

                                        # else:                                                                         #вывод текущей отнормации о размере буфера.
                                        #   print ('\t\t\t' + y.replace(b'\n', b'').decode('utf-8'))

        if interrupts_t:  # если есть хоть один RX-DRP, печатаем  /proc/interrupts
            print_razdel_to_report(b'Interrupts Information (/proc/interrupts):\n',
                                   b'Interrupts Information (/proc/interrupts)\n')

    # статус сенсоров
    razdel_to_report = print_razdel_to_report(b'Sensors system:\n',
                                              b'CP Status - OS (/opt/CPshrd-R77/bin/cpstat -f sensors os)\n')

    if razdel_to_report:
        print('\nSensors system:')
        Sensors_system = True
        for x in razdel_to_report:
            # print(x.decode('utf-8').replace(r' ', '').split('|'))
            if len(x.decode('utf-8').split('|')) > 6:
                # print(x.decode('utf-8').replace(r' ', '').split('|')[5])
                if (x.decode('utf-8').replace(r' ', '').split('|')[5] != '0') and (
                        x.decode('utf-8').replace(r' ', '').split('|')[5] != 'Status'):
                    print('\tSensors: ' + x.decode('utf-8').replace('\n', ' ').replace('|', ' ') + 'Failed')
                    Sensors_system = False
        if Sensors_system:
            print('\tOK')

    report_file.write(b'\n')
    report_file.write(b'==============================================\n')
    report_file.write(b'ClacterXL\n')
    report_file.write(b'==============================================\n')
    print('\n------ ClacterXL ------')

    clacter_ha = True
    # High Availability State (cphaprob state)
    razdel_to_report = print_razdel_to_report(b'High Availability State:\n',
                                              b'High Availability State (cphaprob state)\n')

    if razdel_to_report:
        clacter_ha_true = True
        Cluster_Mode = 'VS'
        for x in razdel_to_report:
            if x == b'HA module not started.\n':
                print('\tClacterXL not started!!!')
                clacter_ha = False

            elif b'Down' in x:
                temp = re.findall(r'(.*Down)', x.decode('utf-8'))[0].split()
                print('\t' + temp[1] + ' - ' + temp[3])
                clacter_ha_true = False

            elif b'Cluster Mode' in x:
                Cluster_Mode = x.replace(b'\n', b'').decode('utf-8')

            elif b'local' in x:
                state_node = x.decode('utf-8').split()[4]


                # if len (re.findall( r'(Standby)', x.decode('utf-8'))) > 0:
                #   temp = re.findall( r'(.*Standby)', x.decode('utf-8'))[0].split()
                #   print('\t' + temp[1] + ' - ' + temp[3])

        if clacter_ha_true and clacter_ha:
            print('\tClacterXL: Enable')
            print('\t' + Cluster_Mode)
            print('\tThis node: ' + state_node)

            # if clacter_ha:
            #   print('\n\tHA module started!!!')

    # Cостояние кластера
    if clacter_ha:
        report_file.write(b'\n')
        report_file.write(b'Cluster state:\n')
        razdel_to_report = selekt_text(b'Cluster state\n')

        if len(razdel_to_report) > 0:
            for x in razdel_to_report:
                if x != b'Current time:\n':
                    report_file.write(b'\t' + x)
                else:
                    break

        else:
            print('\nCluster state:')
            print('\tNO Data Files!!!')

        # High Availability interfaces (cphaprob -a if)
        razdel_to_report = print_razdel_to_report(b'High Availability interfaces:\n',
                                                  b'High Availability interfaces (cphaprob -a if)\n')

        if razdel_to_report:
            print('\nHigh Availability interfaces:')
            interfaces_ha = True
            for x in razdel_to_report:
                if b'DOWN' in x:
                    print('\t' + re.findall(r'(.*DOWN)', x.decode('utf-8'))[0])
                    interfaces_ha = False
            if interfaces_ha:
                print('\tok')

        # High Availability List (cphaprob -l list)

        razdel_to_report = selekt_text(b'High Availability List (cphaprob -l list)\n')
        print('\nHigh Availability List:')

        if razdel_to_report:
            report_file.write(b'\n')
            report_file.write(b'High Availability List:\n')

            ha_list = True
            for x in razdel_to_report:
                # report_file.write(b'\t'+x)
                if b'Device Name:' in x:
                    Device_Name = (re.findall(r'Device Name: (.*)', x.decode('utf-8'))[0])
                if b'Current state:' in x:
                    # print(re.findall(b'Current state: (.*)', x))
                    report_file.write(
                        b'\t' + bytes(Device_Name, 'ascii') + b': ' + (
                            re.findall(b'Current state: (.*)', x)[0]) + b'\n')

                if b'Current state: problem' in x:
                    print('\t' + Device_Name + ': ' + re.findall(r'Current state: (.*)', x.decode('utf-8'))[0])
                    ha_list = False
            if ha_list:
                print('\tOK')

        else:
            print('\tNO Data Files!!!')

        razdel_to_report = selekt_text(b'FireWall-1 Statistics (fw ctl pstat)\n')
        if razdel_to_report:
            print('\nfw ctl pstat:')
            retransmitted = 1
            total = 1
            Sync = False
            for x in razdel_to_report:
                if b'Sync:' in x:
                    Sync = True

                elif Sync and b'retransmitted' in x:
                    retransmitted = int(re.findall(r'retransmitted : (\d+)', x.decode('utf-8'))[0])
                    total = int(re.findall(r'total : (\d+)', x.decode('utf-8'))[0])
                # print ('total = ' + str(total) )
                # print ('retransmitted = ' + str(retransmitted) )


                elif Sync and b'dropped by net' in x:
                    dropped_net = int(re.findall(r'dropped by net : (\d+)', x.decode('utf-8'))[0])
                    # print ('dropped_net = ' + str(dropped_net) )

            if retransmitted / total * 100 > 1:
                print('\ttotal = ' + str(total) + '\tretransmitted = ' + str(retransmitted) + '\tlosses = ' + str(
                    round(retransmitted / total * 100, 2)) + '%')

            elif dropped_net / total * 100 > 1:
                print('\ttotal = ' + str(total) + '\tdropped_net = ' + str(dropped_net) + '\tlosses = ' + str(
                    round(dropped_net / total * 100, 2)) + '%')

            else:
                print('\tSync network - OK')

    # работа CoreXL
    report_file.write(b'\n')
    report_file.write(b'==============================================\n')
    report_file.write(b'CoreXL\n')
    report_file.write(b'==============================================\n')
    print('\n ----- CoreXL ------')

    print_razdel_to_report(b'Interrupts Information (/proc/interrupts):\n',
                           b'Interrupts Information (/proc/interrupts)\n')  # SND/IRQ

    #
    print_razdel_to_report(b'SIM Affinity:\n', b'SIM Affinity\n')

    razdel_to_report = print_razdel_to_report(b'fwkern.conf:\n', b'/opt/CPsuite-R77/fw1/boot/modules/fwkern.conf\n')
    if razdel_to_report:
        print('Настройки ядра:')
        for x in razdel_to_report:
            print('\t' + x.replace(b'\n', b'').decode('utf-8'))

            if b'enable_ssl_multi_core=' in x:
                if x == b'enable_ssl_multi_core=1\n':
                    print('\t' + 'enable MultiCore SSL!')
                else:
                    print('\t' + 'NO enable MultiCore SSL!')

            elif b'fwmultik_dispatch_skip_global=' in x:
                if x == b'fwmultik_dispatch_skip_global=1\n':
                    print('\t' + 'fw_0 освобожден от generic Firewall Worker Core')
                else:
                    print('\t' + 'fw_0 обрабатывает generic Firewall Worker Core!!!')

            elif b'fwha_forw_packet_to_not_active=' in x:
                if x == b'fwha_forw_packet_to_not_active=1\n':
                    print('\t' + 'Разрешен трафик к Standby member of a High Availability cluster')


            elif b'fwmultik_hash_use_dport=' in x:
                if x == b'fwmultik_hash_use_dport=1\n':
                    print('\t' + 'Порт назначения используется для выбора Firewall Worker Core')

    # работа Firewall Worker
    report_file.write(b'\n')
    report_file.write(b'==============================================\n')
    report_file.write(b'Firewall Worker\n')
    report_file.write(b'==============================================\n')
    print('\n ----- Firewall Worker ------')

    razdel_to_report = print_razdel_to_report(b'fw ctl multik stat:\n', b'fw ctl multik stat\n')
    if razdel_to_report:
        print('\nfw ctl multik stat:')
        corexl_enable = True
        corexl_CPU = []
        for x in razdel_to_report:
            if x == b'fw: CoreXL is disabled\n':
                print('\tCoreXL is disabled')
                corexl_enable = False

            elif (re.findall(r'(\d+)', x.decode('utf-8').split('|')[0])):
                corexl_CPU.append(int(x.decode('utf-8').split('|')[2]))

        if corexl_enable:
            print('\tenable')
            # print (corexl_CPU)
            # print (len(corexl_CPU))
            # print ( str(CPUs))
            print('\n\tFirewall Worker user ' + str(len(corexl_CPU)) + ' of ' + str(CPUs) + ' CPUs')

            #
            print_razdel_to_report(b'fw affinity:\n', b'fw affinity -l -a -v\n')

    # ручная настройка affinity
    razdel_to_report = print_razdel_to_report(b'fwaffinity.conf:\n', b'/opt/CPsuite-R77/fw1/conf/fwaffinity.conf\n')
    if razdel_to_report:
        print('\nfwaffinity.conf:')
        for x in razdel_to_report:
            if len(re.findall(b'^#', x)) < 1:
                if x == b'i default auto\n':
                    print('\taffinity config auto assigning - OK')
                else:
                    print('\t' + x.replace(b'\n', b'').decode(
                        'utf-8') + '\t\t-\t?')  # нестандартные настройки, надо проверять!!!

    # FW
    report_file.write(b'\n')
    report_file.write(b'==============================================\n')
    report_file.write(b'Accelerator FW\n')
    report_file.write(b'==============================================\n')
    print('\n ----- Accelerator FW ------')

    # FW-1 Accelerator
    razdel_to_report = print_razdel_to_report(b'FW-1 Accelerator:\n', b'FW-1 Accelerator status\n')
    if razdel_to_report[
        0] == b'Usage: fwaccel on | off | ver | stat | notifstats | conns | templates | conns_limit | dbg <...> | help\n':
        razdel_to_report = []
    # print(razdel_to_report)
    if len(razdel_to_report) > 4:
        for x in razdel_to_report:
            if x == b'Accelerator Status : off\n':
                print('\t' + x.replace(b'\n', b'').decode('utf-8') + '\t-\t!!!!!')
                accelerator = False
                accelerator_vpn = False

            elif x == b'Accelerator Status : on\n':
                accelerator = True

            if b'Accelerator Features' in x:
                accelerator = False

            if accelerator:
                print('\t' + x.replace(b'\n', b'').decode('utf-8'))

            if b'Cryptography Features' in x:
                print('\tAccelerator VPN\t   : on')
                accelerator_vpn = True

        if not accelerator_vpn:
            print('\tAccelerator VPN\t   : off')

    # fwaccel stats -s
    razdel_to_report = print_razdel_to_report(b'fwaccel stats -s:\n', b'fwaccel stats -s\n')

    if razdel_to_report:
        for x in razdel_to_report:
            # print(x)
            if b'Accelerated pkts' in x:
                Total_pkts = int(re.findall(r'/(\d+)', x.decode('utf-8'))[0])
                # print (Total_pkts)

    # FireWall-1 Statistics (fw ctl pstat)
    razdel_to_report = print_razdel_to_report(b'FireWall-1 Statistics (fw ctl pstat):\n',
                                              b'FireWall-1 Statistics (fw ctl pstat)\n')
    if razdel_to_report:
        print('\nfw ctl pstat:')
        hmem = False
        smem = False
        kmem = False

        for x in razdel_to_report:
            # if len (re.findall( r'(Aggressive Aging)', x.decode('utf-8'))) > 0:
            if b'Aggressive Aging' in x:
                print('\t' + x.replace(b'\n', b'').lstrip().decode('utf-8') + '\n')

            elif b'Hash kernel memory' in x:
                hmem = True

            elif hmem and b'failed alloc' in x:
                a = re.findall(r'(\d+) failed alloc', x.decode('utf-8'))[0]

                if a != '0':
                    a = a + ' failed alloc - Warning'
                else:
                    a = a + ' failed alloc - OK'
                print('\tHash kernel memory\t=\t' + a)

                hmem = False


            elif b'System kernel memory' in x:
                smem = True

            elif smem and b'failed alloc' in x:
                a = re.findall(r'(\d+) failed alloc', x.decode('utf-8'))[0]

                if a != '0':
                    a = a + ' failed alloc - False!!!'
                else:
                    a = a + ' failed alloc - OK'
                print('\tSystem kernel memory\t=\t' + a)
                smem = False


            elif b'Kernel memory' in x:
                kmem = True

            elif kmem and b'failed alloc' in x:
                a = re.findall(r'(\d+) failed alloc', x.decode('utf-8'))[0]

                if a != '0':
                    a = a + ' failed alloc - False!!!'
                else:
                    a = a + ' failed alloc - OK'
                print('\tKernel memory\t\t=\t' + a)

                kmem = False


            elif b'fragments' in x:
                # print(x)
                # print(Total_pkts)
                fragments = int(re.findall(r'(\d+) packets', x.decode('utf-8'))[0])

                # if fragments / Total_pkts * 100 > 5:
                print('\n\tfragments packets = ' + str(fragments) + ' of ' + str(Total_pkts) + ' (' + str(
                    round(fragments / Total_pkts * 100, 2)) + '%)')

    for x in enabled_blades:
        # print (razdelit_for_sample_1)
        print('\n ----- ' + x + ' ----- \n')

        if x == 'fw':
            razdel_to_report = print_razdel_to_report(b'FireWall-1 Status:\n', b'FireWall-1 Status\n')
            fw_status = razdel_to_report[1].decode('utf-8').split()
            print('\tPolicy ' + fw_status[2] + ' install to ' + fw_status[3] + ' ' + fw_status[4])

        # print ('\tpolisi')


        elif x == 'ips':
            razdel_to_report = selekt_text(b'/opt/CPsuite-R77/fw1/database/myself_objects.C\n')
            a = False
            b = False
            for y in razdel_to_report:
                if b':SD_profile' in y:
                    a = True

                elif a and b':Name (' in y:
                    print('\t' + 'IPS Profile: ' + (re.findall(r'\((.*)\)', y.decode('utf-8'))[0]))
                    a = False

                elif b':protect_internal_interfaces_only (' in y:
                    if (re.findall(r'\((.*)\)', y.decode('utf-8'))[0]) == 'true':
                        print('\t' + 'Protect internal hosts only')
                    else:
                        print('\t' + 'Perform IPS inspection on all traffic - !!!')
                    break

            razdel_to_report = selekt_text(b'/opt/CPsuite-R77/fw1/database/slim_rules.C\n')
            if len(razdel_to_report) > 1:
                for y in razdel_to_report:
                    if b'sd_update_version' in y:
                        a = True

                    elif a:
                        if b'val' in y:
                            version = (re.findall(r'\((.*)\)', y.decode('utf-8'))[0])
                            print('\t' + 'IPS Version: ' + version)
                            a = False


                    elif b'sd_last_update_time' in y:
                        b = True

                    elif b:
                        if b'val' in y:
                            time_up = (re.findall(r'\((.*)\)', y.decode('utf-8'))[0])
                            # print('Update time: ' + time.localtime(version))
                            # print(time_up)
                            # print('Update time: ' + time.ctime(int(time_up)))   #Thu Oct 20 03:03:00 2016

                            print('\t' + 'Last Update: ' + str(datetime.datetime.fromtimestamp(int(time_up))))
                            b = False

            razdel_to_report = selekt_text(b'IPS Status\n')
            if len(razdel_to_report) > 1:
                for y in razdel_to_report:
                    if b'Global Detect:' in y:
                        print('\t' + y.replace(b'\n', b'').decode('utf-8'))
                    elif b'Bypass Under Load:' in y:
                        print('\t' + y.replace(b'\n', b'').decode('utf-8'))


                        # print

        elif x == 'vpn':
            razdel_to_report = selekt_text(b'/opt/CPsuite-R77/fw1/conf/Standard.pf\n')
            if len(razdel_to_report) > 1:
                razdel_to_report = print_razdel_to_report(b'/opt/CPsuite-R77/fw1/conf/Standard.pf\n',
                                                          b'/opt/CPsuite-R77/fw1/conf/Standard.pf\n')
                vpn_methods_true = False
                vpn_methods = []
                for y in razdel_to_report:

                    if b'vpn_methods' in y:
                        vpn_methods_true = True

                    elif b'};' in y:
                        vpn_methods_true = False

                    elif vpn_methods_true:
                        # print (y.split())
                        vpn_methods.append(re.findall(r'(\d+);', y.decode('utf-8'))[0])
                        # print (vpn_methods)

                for y in vpn_methods:
                    razdel_to_report = selekt_text(b'/opt/CPsuite-R77/fw1/database/communities_objects.C\n')
                    if len(razdel_to_report) > 1:
                        for z in razdel_to_report:
                            if re.findall(br'^\t: \((.+)', z):
                                name_vpn = re.findall(r'^\t: \((.+)', z.decode('utf-8'))[0]
                            # print (name_vpn)
                            # print(z)
                            if re.findall(r'\t\t:ID \((\d+)\)', z.decode('utf-8')):
                                if re.findall(r'\t\t:ID \((\d+)\)', z.decode('utf-8'))[0] == y:
                                    vpn_methods[vpn_methods.index(y)] = name_vpn
                                    # print (vpn_methods)
                                    break

                print('Participates in VPN Communities:')
                for y in vpn_methods:
                    print('\t' + str(vpn_methods.index(y) + 1) + ': ' + y)

                # else:
                #   print('\t' + y.replace(b'\n',b'').decode('utf-8') )

                razdel_to_report = selekt_text(b'/opt/CPsuite-R77/fw1/conf/Standard.pf\n')
                if len(razdel_to_report) > 1:
                    vpn_routing_true = False
                    vpn_routing = []
                    for y in razdel_to_report:

                        if b'vpn_routing' in y:
                            vpn_routing_true = True

                        elif b'};' in y:
                            vpn_routing_true = False

                        elif vpn_routing_true:
                            # print (y.split())
                            vpn_routing.append(y.decode('utf-8'))
                            # print (vpn_methods)

                    # print (vpn_routing)


                    print('\nVpn routing:')  # VPN routing     fw tab -t vpn_routing
                    for y in vpn_routing:
                        vpn_routing_1 = (re.findall(r'(\d{1,2}.\d{1,2}.\d{1,2}.\d{1,2})', y))
                        print('\t' + vpn_routing_1[0] + '\t' + vpn_routing_1[1] + '\tGateway : ' + vpn_routing_1[2])


            else:
                razdel_to_report = selekt_text(b'/opt/CPsuite-R77/fw1/database/communities_objects.C\n')
                if len(razdel_to_report) > 1:
                    hostname_vpn = ':Name (' + hostname_r + ')'
                    # print(hostname_vpn)

                    participants_domains = False
                    vpn_used = False

                    for y in razdel_to_report:
                        if re.findall(br'^\t: \((.+)', y):
                            if participants_domains:
                                print('\t' + name_vpn)
                                vpn_used = True

                            name_vpn = re.findall(r'^\t: \((.+)', y.decode('utf-8'))[0]
                            participants_domains = False
                        # print (name_vpn)
                        # print(z)

                        elif b':topology' in y:
                            name_vpn = name_vpn + ' - ' + re.findall(r'\((.+)\)', y.decode('utf-8'))[0]
                        # print (name_vpn)

                        # elif b':participants_domains'in y :
                        #   participants_domains = True

                        # elif  hostname_vpn in y.decode('utf-8') and participants_domains :
                        #   print('\t' + name_vpn)
                        #   participants_domains = False

                        elif hostname_vpn in y.decode('utf-8'):
                            participants_domains = True

                    if not vpn_used:
                        print('\tnot community')

            razdel_to_report = selekt_text(b'/opt/CPsuite-R77/fw1/database/myself_objects.C\n')
            if len(razdel_to_report) > 1:
                Use_Probing = False
                misp_active = True
                misp_apply_to_vpn = False
                IP_list = False
                VPN_IP_list = []
                print('\nConfig:')

                for y in razdel_to_report:

                    if b':misp_active (false)' in y:
                        misp_active = False
                    elif misp_active and b':misp_apply_to_vpn (true)' in y:  # если misp_apply_to_vpn = true , то настройки Link Selektion берутся из ISP Redundancy
                        print('\n\tLink Selektion = ISP Redundancy')
                        misp_apply_to_vpn = True
                        break


                    elif b':ip_resolution_mechanism ' in y:
                        if b'ongoingProb' in y:
                            print('\n\tUse Probing')
                            Use_Probing = True

                        elif b'dnsLookup' in y:
                            print('\n\tUse DNS resolving')  # хранится в :dns_IP_resolution

                        elif b'topologyCalc' in y:
                            print('\n\tCalculate ip based on network topology')

                        elif b'mainIpVpn' in y:
                            print('\n\tAlways use this IP address: Main address')

                        elif b'singleIpVpn' in y:
                            print('\n\tAlways use this IP address: Selected address')  # хранится в :single_VPN_IP

                        elif b'singleNATIpVPN' in y:
                            print('\n\tAlways use this IP address: Statically NATed IP')  # хранится в :single_VPN_IP


                    elif b':dns_IP_resolution ' in y:
                        print('\t' + re.findall(r'\((.+)\)', y.decode('utf-8'))[0])


                    elif b':single_VPN_IP ' in y:
                        print('\t' + re.findall(r'\((.+)\)', y.decode('utf-8'))[0])

                    if Use_Probing:
                        if b':link_selection_mode' in y:
                            link_selection_mode = re.findall(r'\((.+)\)', y.decode('utf-8'))[0]

                        elif b':available_VPN_IP_list (' in y:
                            IP_list = True

                        elif IP_list and b'\t)' in y:
                            IP_list = False

                        elif IP_list and b': (' in y:
                            VPN_IP_list.append(re.findall(r'\((.+)\)', y.decode('utf-8'))[0])

                if Use_Probing and not misp_apply_to_vpn:
                    print('\n\tlink selection mode:\t' + link_selection_mode)
                    print('\tProbe the following addresses:')
                    for y in VPN_IP_list:
                        print('\t\t' + y)

            razdel_to_report = selekt_text(b'/opt/CPsuite-R77/fw1/database/myself_objects.C\n')
            vpn_manual = False
            manual_encdomain = False
            if len(razdel_to_report) > 1:
                for y in razdel_to_report:
                    if b':encdomain' in y:
                        if b'manual' in y:
                            vpn_manual = True
                        else:
                            print("\n\tVPN Domain: All IP Addresses")

                    elif vpn_manual and b':manual_encdomain' in y:
                        manual_encdomain = True

                    elif manual_encdomain and b'refname' in y:
                        print("\n\tVPN Domain: manual " + re.findall(r'\((.+)\)', y.decode('utf-8'))[0])


        elif x == 'identityServer':
            razdel_to_report = print_razdel_to_report(b'identityServer:\n',
                                                      b'CP Status - IDENTITYSERVER (/opt/CPshrd-R77/bin/cpstat -f default identityServer)\n')
            if razdel_to_report:
                for x in razdel_to_report:
                    print('\t' + x.replace(b'\n', b'').decode('utf-8'))


        elif x == 'av' or x == 'anti_bot':
            razdel_to_report = print_razdel_to_report(b'antimalware:\n',
                                                      b'CP Status - ANTIMALWARE (/opt/CPshrd-R77/bin/cpstat -f default antimalware)\n')
            if razdel_to_report:
                for x in razdel_to_report:
                    if re.findall(br'status:.*failed', x):
                        print('\t' + x.replace(b'\n', b'').decode('utf-8') + '   -   !!!')
                    else:
                        print('\t' + x.replace(b'\n', b'').decode('utf-8'))

            razdel_to_report = print_razdel_to_report(b'FireWall-1 Status - Anti Malware:\n',
                                                      b'FireWall-1 Status - Anti Malware\n')
            if razdel_to_report:
                for x in razdel_to_report:
                    if b'Policy' in x:
                        print('\t' + x.replace(b'\n', b'').decode('utf-8'))

            razdel_to_report = selekt_text(b'/opt/CPsuite-R77/fw1/conf/anti_malware_rulebase.C\n')
            if razdel_to_report:
                for x in razdel_to_report:
                    if b':last_modified_utc' in x:
                        time_up = (re.findall(r'\((.*)\)', x.decode('utf-8'))[0])
                        print('\tLastModified: ' + str(datetime.datetime.fromtimestamp(int(time_up))))


        elif x == 'urlf':
            razdel_to_report = print_razdel_to_report(b'urlf:\n',
                                                      b'CP Status - URLF (/opt/CPshrd-R77/bin/cpstat -f update_status urlf)\n')
            if razdel_to_report:
                for x in razdel_to_report:
                    if re.findall(br'status:.*failed', x):
                        print('\t' + x.replace(b'\n', b'').decode('utf-8') + '   -   !!!')
                    else:
                        print('\t' + x.replace(b'\n', b'').decode('utf-8'))

            razdel_to_report = selekt_text(b'/opt/CPsuite-R77/fw1/conf/rad_services.C\n')
            if razdel_to_report:
                for x in razdel_to_report:
                    if b':last_modified_utc' in x:
                        time_up = (re.findall(r'\((.*)\)', x.decode('utf-8'))[0])
                        print('\tLastModified:\t\t ' + str(datetime.datetime.fromtimestamp(int(time_up))))
                        break

        elif x == 'appi':
            razdel_to_report = print_razdel_to_report(b'appi:\n',
                                                      b'CP Status - APPI (/opt/CPshrd-R77/bin/cpstat -f update_status appi)\n')
            if razdel_to_report:
                for x in razdel_to_report:
                    if re.findall(br'status:.*failed', x):
                        print('\t' + x.replace(b'\n', b'').decode('utf-8') + '   -   !!!')
                    else:
                        print('\t' + x.replace(b'\n', b'').decode('utf-8'))

            razdel_to_report = selekt_text(b'/opt/CPsuite-R77/fw1/conf/rad_services.C\n')
            if razdel_to_report:
                for x in razdel_to_report:
                    if b':last_modified_utc' in x:
                        time_up = (re.findall(r'\((.*)\)', x.decode('utf-8'))[0])
                        print('\tLastModified:\t\t ' + str(datetime.datetime.fromtimestamp(int(time_up))))
                        break


if __name__ == "__main__":
    sample_from_cpinfo(cpinfo_file, selekt)

    report_file = open(report, 'wb')
    generation_file_report()
    report_file.close()

    # finish =  time.time()

    # print(finish-start)
