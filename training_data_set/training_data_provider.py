import csv
import sys,os
import configurations


class TrainingDataProvider(object):
    def __init__(self):
        self.TRAINING_DATA_FILES_PATH = [
            configurations.PROJECT_ROOT + "/data_set/1.csv",
            configurations.PROJECT_ROOT + "/data_set/2.csv",
            configurations.PROJECT_ROOT + "/data_set/3.csv",
            configurations.PROJECT_ROOT + "/data_set/4.csv",
            configurations.PROJECT_ROOT + "/data_set/5.csv"
        ]
        self.HUGE_COMMENTS_FILE = configurations.PROJECT_ROOT + "/data_set/huge.csv"
        self.ALL_SPAM_COMMENTS_FILE = configurations.PROJECT_ROOT + "/data_set/spam.txt"
        self.ALL_HAM_COMMENTS_FILE = configurations.PROJECT_ROOT + "/data_set/ham.txt"
        self.spam_comments = []
        self.ham_comments = []
        self._create_training_data()

    def _create_training_data(self):
        print "[TrainingDataProvider] Creating training data set."
        if self.training_data_files_available():
            self.spam_comments = self.read_spam_from_file()
            self.ham_comments = self.read_ham_from_file()
            return
        else:
            for filepath in self.TRAINING_DATA_FILES_PATH:
                self._read_CSV_file(filepath)
            # self.read_big_csv_file()
            print "Training completed./n Creating data files."
            self.create_data_files()
            print "Data files created."

    def training_data_files_available(self):
        return os.path.exists(self.ALL_SPAM_COMMENTS_FILE) and os.path.exists(self.ALL_HAM_COMMENTS_FILE)

    def _read_CSV_file(self, filepath):
        row_count = 0
        with open(filepath) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                row_count += 1

                # ignore first row because it has column names and not actual data
                if row_count == 1:
                    continue

                comment = row[3]
                # 1 = spam, 0 = ham
                is_spam = int(row[4]) == 1

                if is_spam:
                    self.spam_comments.append(comment)
                else:
                    self.ham_comments.append(comment)

    def read_big_csv_file(self):
        with open(self.HUGE_COMMENTS_FILE) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                comment = row[3]
                # 1 = spam, 0 = ham
                is_spam = row[4] == "TRUE"

                if is_spam:
                    self.spam_comments.append(comment)
                else:
                    self.ham_comments.append(comment)

    def get_spam_comments(self):
        if len(self.spam_comments) == 0:
            raise RuntimeError("Training not complete. spam is empty.")
        else:
            return self.spam_comments

    def get_ham_comments(self):
        if len(self.ham_comments) == 0:
            raise RuntimeError("Training not complete. ham is empty.")
        else:
            return self.ham_comments

    # first partition % comments are used as training data and remaining as training data
    def get_test_ham_comments(self):
        all_ham = self.get_ham_comments()
        ham_count = len(all_ham)
        partition = ham_count * 0.20

        return all_ham[:partition]

    def get_test_spam_comments(self):
        all_spam = self.get_spam_comments()
        spam_count = len(all_spam)
        partition = spam_count * 0.20

        return all_spam[:partition]

    def get_training_ham_comments(self):
        all_ham = self.get_ham_comments()
        ham_count = len(all_ham)
        partition = ham_count * 0.20

        return all_ham[partition:]

    def get_training_spam_comments(self):
        all_spam = self.get_spam_comments()
        spam_count = len(all_spam)
        partition = spam_count * 0.20

        return all_spam[partition:]

    def read_spam_from_file(self):
        spam_comments = []
        with open(self.ALL_SPAM_COMMENTS_FILE, "r") as spam_file:
            spam_comments = spam_file.readlines()
        return spam_comments

    def read_ham_from_file(self):
        ham_comments = []
        with open(self.ALL_HAM_COMMENTS_FILE, "r") as ham_file:
            ham_comments = ham_file.readlines()
        return ham_comments

    # read all test data and create separate files for ham and spam comments.
    def create_data_files(self):
        print "Creating spam comments file."
        all_spam = self.get_spam_comments()
        with open(self.ALL_SPAM_COMMENTS_FILE, "w+") as f:
            for item in all_spam:
                f.write("%s\n" % item)
        f.close()

        print "Creating ham comments file."
        all_ham = self.get_ham_comments()
        with open(self.ALL_HAM_COMMENTS_FILE, "w+") as f:
            for item in all_ham:
                f.write("%s\n" % item)
        f.close()
        print "spam and ham comment txt files created successfully."