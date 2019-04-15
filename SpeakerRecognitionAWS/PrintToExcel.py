import xlsxwriter

def print_to_excel(transcriptData):
    workbook = xlsxwriter.Workbook('hello.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "Username:")
    worksheet.write(0, 1, transcriptData["userName"])

    worksheet.write(1, 0, "File Name:")
    worksheet.write(1, 1, transcriptData["fileName"])

    worksheet.write(2, 0, "File URL:")
    worksheet.write(2, 1, transcriptData["fileURL"])

    worksheet.write(3, 0, "File Content:")
    worksheet.write(3, 1, transcriptData["fileContentType"])

    worksheet.write(4, 0, "File Description:")
    worksheet.write(4, 1, transcriptData["fileDescription"])

    worksheet.write(5, 0, "Multipl Speakers:")
    worksheet.write(5, 1, transcriptData["multipleSpeakersBoolean"])

    worksheet.write(6, 0, "Number of Speakers:")
    worksheet.write(6, 1, transcriptData["numberOfSpeakersInteger"])

    worksheet.write(7, 0, "Multiple Channels:")
    worksheet.write(7, 1, transcriptData["multipleChannelsBoolean"])

    worksheet.write(9, 0, "Transcript:")

    row = 10
    for word in transcriptData["transcript"]:
        row = row + 1
        currentIndex = "A" + str(row)
        worksheet.write(currentIndex, word)

    # skip two rows
    row = row + 2
    worksheet.write(row, 0, "Accuracy")
    worksheet.write(row, 1, "Number of words")
    worksheet.write(row, 2, "Percentage")
    statsIteration = 0
    row = row + 1
    for stats in transcriptData["statistics"]:
        for stat in stats:
            statsIteration = statsIteration + 1
            if statsIteration == 1:
                worksheet.write(row, 0, stat)
            elif statsIteration == 2:
                worksheet.write(row, 1, stat)
            else:
                worksheet.write(row, 2, stat)
                # move to next row once 3 items in list are done
                row = row + 1
                # reset count
                statsIteration = 0
    workbook.close()
