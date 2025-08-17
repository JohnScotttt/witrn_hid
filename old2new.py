def old_to_new(old_csv_path, new_csv_path):
    try:
        old = open(old_csv_path, 'rb')
        new = open(new_csv_path, 'wb')
        lines = old.readlines()
        length = len(lines)
        total_time = lines[length - 1].strip().split(b",")[0]
        total_time = total_time[:9] + b"." + total_time[10:]
        new.write(b'\xef\xbb\xbf')  # Write BOM for UTF-8
        for i, line in enumerate(lines):
            if i == 0:
                sample_sum = int(line.strip().split(b",")[1])
                new_line = b"SUM," + str(sample_sum).encode() + b"\r\n"
            elif i == 1:
                new_line = b"TotalTime,=" + total_time + b"\r\n"
            elif i == 2:
                new_line = b"SampTime(ms),10\r\n"
            elif i == 3:
                new_line = line[:9] + line[10:] + b"\r\n"
            elif i == 4:
                new_line = b"Time(D.hh:mm:ss.ms),Voltage(V),Current(A),Power(W),Temp(\xc2\xb0C),\r\n"
            else:
                l = [x.strip() for x in line.strip().split(b",")]
                if l[4] == b"--":
                    l[4] = b"0.0"
                l[0] = b"=" + l[0][:9] + b"." + l[0][10:]
                new_line = b",".join(l) + b",\r\n"
            new.write(new_line)
    except Exception as e:
        print(f"Error opening files: {e}")
    finally:
        if 'old' in locals():
            old.close()
        if 'new' in locals():
            new.close()

if __name__ == "__main__":
    old_to_new("酷态科10号充电宝自充2.csv",
               "酷态科10号充电宝自充2_new.csv")