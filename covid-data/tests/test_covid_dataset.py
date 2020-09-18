import pytest
from models import CovidDataset
from utils import constants

@pytest.fixture()
def normal_dataset():
    normal_dataset = [
        ["2020-03-21", 1], ["2020-03-22", 1],
        ["2020-03-23", 1], ["2020-03-24", 1],
        ["2020-03-25", 2], ["2020-03-26", 3],
        ["2020-03-27", 5], ["2020-03-28", 5],
        ["2020-03-29", 5], ["2020-03-30", 6],
        ["2020-03-31", 6], ["2020-04-01", 10],
        ["2020-04-02", 15], ["2020-04-03", 22],
        ["2020-04-04", 22], ["2020-04-05", 25],
        ["2020-04-06", 27], ["2020-04-07", 28],
        ["2020-04-08", 29], ["2020-04-09", 30],
        ["2020-04-10", 31], ["2020-04-11", 32],
        ["2020-04-12", 33], ["2020-04-13", 34],
        ["2020-04-14", 35], ["2020-04-15", 36],
        ["2020-04-16", 37], ["2020-04-17", 38]]
    yield normal_dataset 

@pytest.fixture()
def normal_dataset_zero_start():
    starts_with_0_dataset = [
        ["2020-03-21", 0], ["2020-03-22", 0],
        ["2020-03-23", 0], ["2020-03-24", 0],
        ["2020-03-25", 0], ["2020-03-26", 3],
        ["2020-03-27", 5], ["2020-03-28", 5],
        ["2020-03-29", 5], ["2020-03-30", 6],
        ["2020-03-31", 6], ["2020-04-01", 10],
        ["2020-04-02", 15], ["2020-04-03", 22],
        ["2020-04-04", 22], ["2020-04-05", 25],
        ["2020-04-06", 27]]
    yield starts_with_0_dataset 

class TestDataset:

    def test_get_first_positive(self, normal_dataset):
        assert CovidDataset(normal_dataset)\
            .get_first_positive() == "2020-03-21"

    def test_get_first_positive_starts_with_zero(self, \
        normal_dataset_zero_start):
        assert CovidDataset(normal_dataset_zero_start)\
            .get_first_positive() == "2020-03-26"

    def test_get_max_case_day(self, normal_dataset):
        assert CovidDataset(normal_dataset)\
            .get_max_case_day() == "2020-04-03"

    def test_get_worst_n_days(self, normal_dataset):
        assert CovidDataset(normal_dataset)\
            .get_worst_n_days(constants.DAYS_IN_WEEK) \
                == ("2020-03-31", "2020-04-06")
