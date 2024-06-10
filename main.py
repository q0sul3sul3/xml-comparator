import csv

import xmltodict


def parse_xml(file_path, encoding='big5'):
    with open(file_path, 'r', encoding=encoding) as file:
        xml_content = file.read()
    return xmltodict.parse(xml_content)


def extract_hdata(xml_dict):
    data = {}
    for hdata in xml_dict['patient']['hdata']:
        h9 = hdata['h9']
        h7 = str(hdata['h7'])
        h11 = hdata['h11']
        h15 = hdata['h15']
        key = (h9, h7, h11, h15)
        if key not in data:
            rdata = hdata['rdata']
            if isinstance(rdata, dict):
                rdata = [rdata]

            data[key] = [{'r1': r['r1'], 'r2': r['r2'], 'r4': r['r4']} for r in rdata]
    return data


def compare_hdata(data1, data2):
    results = []
    commen_keys = set(data1.keys()).intersection(set(data2.keys()))
    for key in commen_keys:
        h9, h7, h11, h15 = key
        rdata1 = data1[key]
        rdata2 = data2[key]
        results.append((h9, h7, h11, h15, 'data1', rdata1))
        results.append((h9, h7, h11, h15, 'data2', rdata2))

    for key in data1.keys():
        if key not in commen_keys:
            h9, h7, h11, h15 = key
            rdata1 = data1[key]
            results.append((h9, h7, h11, h15, 'data1', rdata1))

    for key in data2.keys():
        if key not in commen_keys:
            h9, h7, h11, h15 = key
            rdata2 = data2[key]
            results.append((h9, h7, h11, h15, 'data2', rdata2))

    return results


def write_to_csv(results, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        rows = []
        for row in results:
            hdata, rdata = row[0:-1], row[-1]
            rows.append(hdata + tuple(value for d in rdata for value in d.values()))

        writer.writerows(rows)


def main(file1, file2, output_file):
    xml_dict1 = parse_xml(file1)
    xml_dict2 = parse_xml(file2)
    data1 = extract_hdata(xml_dict1)
    data2 = extract_hdata(xml_dict2)
    results = compare_hdata(data1, data2)
    write_to_csv(results, output_file)


if __name__ == '__main__':
    file1 = 'file1.xml'
    file2 = 'file2.xml'
    output_file = 'output_file.csv'
    main(file1, file2, output_file)
