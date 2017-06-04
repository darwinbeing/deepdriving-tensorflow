import dd.data_reader as dddr
import argparse
import cv2

Parser = argparse.ArgumentParser('Read the original DeepDriving training data.')
Parser.add_argument('path', help="The path to the DeepDriving training data.")

Arguments = Parser.parse_args()
TrainingDataPath = Arguments.path

DataReader = dddr.CDataReader(TrainingDataPath)

print("First Key in Database: {}".format(DataReader.FirstKey))
print("Last Key in Database: {}".format(DataReader.LastKey))

with DataReader.getCursor() as Cursor:
    while Cursor.Valid:
        print("")
        print("Key: {}".format(Cursor.Key))
        print("ImageWidth: {}".format(Cursor.ImageWidth))
        print("ImageHeight: {}".format(Cursor.ImageHeight))
        print("Labels:")
        print(Cursor.Labels)
        cv2.imshow("Image", Cursor.Image)
        if cv2.waitKey(0) == 27:
            break

        Cursor.next()

