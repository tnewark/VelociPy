def create_report_index(reports):
    return {r['@ReportTitle']: r['@ReportId'] for r in reports['Reports']['Report']}


def main():
    pass


if __name__ == '__main__':
    main()
