import dd.data_reader as dddr
import argparse

Parser = argparse.ArgumentParser('Read the original DeepDriving training data.')
Parser.add_argument('path', help="The path to the DeepDriving training data.")

Arguments = Parser.parse_args()
TrainingDataPath = Arguments.path

DataReader = dddr.CDataReader(TrainingDataPath)

print("First Key in Database: {}".format(DataReader.FirstKey))
print("Last Key in Database: {}".format(DataReader.LastKey))

with DataReader.getCursor() as Cursor:
    print("")
    print("Key: {}".format(Cursor.Key))
    print("ImageWidth: {}".format(Cursor.ImageWidth))
    print("ImageHeight: {}".format(Cursor.ImageHeight))

