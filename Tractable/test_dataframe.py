import pipeline

## Check if number of customer in table is correct
def test_count_customers():
    assert pipeline.dfCustomers.count() == 137

def test_count_products():
    assert pipeline.dfProducts.count() == 64

def test_count_all_trans():
    assert pipeline.df.count() == 4497

def test_count_purchase_count():
    assert pipeline.df2.count() != 4497

def tes_impotr():
    assert pipeline.import_file("customers.csv") == True
