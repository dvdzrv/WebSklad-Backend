def parse():
    string = ""

    with open('db/csvs/tabulka.csv', "r", encoding="utf-8") as csv_file:
        import csv
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                for i in range(len(row)):
                    if row[i] == "":
                        row[i] = "NULL"
                string += f"(NULL, \"{row[1]}\", \"{row[2]}\", \"{row[3]}\", \"{row[4]}\", {row[5]}, {row[6]}),"
                line_count += 1
        print(f'Processed {line_count} lines.')

    #part_id, category, sub_category, name, value, count, min_count


    string = string[:-1]
    return string






if __name__ == "__main__":
    print(parse())
