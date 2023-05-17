from yellow_taxi_data.database.postgres import DatabaseEngine, Timescale


def test_timescale_engine(mocker):
    """Test Timescale engine is the same as DatabaseEngine."""
    mocker.patch("yellow_taxi_data.database.postgres.DatabaseEngine.create_engine")
    timescale = Timescale().engine
    assert isinstance(timescale, DatabaseEngine)


def test_timescale_singleton(mocker):
    """Test whether the Timescale class is a singleton."""
    mocker.patch("yellow_taxi_data.database.postgres.DatabaseEngine.create_engine")
    timescale1 = Timescale().engine
    timescale2 = Timescale().engine
    assert timescale1 is timescale2
