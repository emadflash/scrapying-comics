import sys
sys.path.append('../src/')

from extract_csv import write_metadata_to_file

write_metadata_to_file("../urls.txt", '../test_dataset.csv', 1, 10)
