import pytest
from datetime import datetime
from backend.app.crud.bls import fetch_bls_data, process_bls_series_data, BLSError

# Test data
TEST_SERIES = {
    "CPI": "CUUR0000SA0",
    "Nonfarm Payrolls": "CES0000000001",
    "Initial Claims": "ICSA"
}

@pytest.fixture
def current_year():
    return str(datetime.now().year)

@pytest.fixture
def start_year(current_year):
    return str(int(current_year) - 4)

def test_fetch_bls_data(start_year, current_year):
    """Test fetching data from BLS API"""
    try:
        bls_data = fetch_bls_data(
            series_ids=list(TEST_SERIES.values()),
            start_year=start_year,
            end_year=current_year
        )
        
        assert bls_data is not None
        assert 'Results' in bls_data
        assert 'series' in bls_data['Results']
        assert len(bls_data['Results']['series']) > 0
        
        # Test data structure
        series = bls_data['Results']['series'][0]
        assert 'seriesID' in series
        assert 'data' in series
        assert len(series['data']) > 0
        
        # Test data point structure
        data_point = series['data'][0]
        assert 'year' in data_point
        assert 'period' in data_point
        assert 'value' in data_point
        
    except BLSError as e:
        pytest.fail(f"BLS API error: {str(e)}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {str(e)}")

def test_process_bls_series_data():
    """Test processing BLS series data"""
    # Sample series data
    series_data = {
        'data': [
            {
                'year': '2024',
                'period': 'M03',
                'value': '309.99',
                'footnotes': [{'text': 'Preliminary'}]
            },
            {
                'year': '2024',
                'period': 'M02',
                'value': '309.12',
                'footnotes': [{'text': 'Final'}]
            },
            {
                'year': '2023',
                'period': 'M03',
                'value': '308.44',
                'footnotes': []
            }
        ]
    }
    
    result = process_bls_series_data(series_data)
    
    assert result is not None
    assert 'value' in result
    assert 'year' in result
    assert 'period' in result
    assert 'footnotes' in result
    assert 'change' in result
    
    # Test specific values
    assert result['value'] == 309.99
    assert result['year'] == 2024
    assert result['period'] == 'M03'
    assert 'Preliminary' in result['footnotes']
    
    # Test year-over-year change calculation
    assert isinstance(result['change'], float)
    assert result['change'] == ((309.99 - 308.44) / 308.44) * 100

def test_process_bls_series_data_empty():
    """Test processing empty BLS series data"""
    empty_data = {'data': []}
    result = process_bls_series_data(empty_data)
    assert result is None

def test_process_bls_series_data_invalid():
    """Test processing invalid BLS series data"""
    # Test with missing value field
    invalid_data = {
        'data': [
            {
                'year': '2024',
                'period': 'M03',
                'footnotes': []
            }
        ]
    }
    result = process_bls_series_data(invalid_data)
    assert result is None

    # Test with invalid value format
    invalid_data = {
        'data': [
            {
                'year': '2024',
                'period': 'M03',
                'value': 'invalid',
                'footnotes': []
            }
        ]
    }
    result = process_bls_series_data(invalid_data)
    assert result is None

    # Test with empty data array
    invalid_data = {'data': []}
    result = process_bls_series_data(invalid_data)
    assert result is None

if __name__ == '__main__':
    pytest.main([__file__]) 