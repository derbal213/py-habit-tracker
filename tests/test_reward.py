from app.database.models import Reward

def test_basic_insert():
    reward: Reward = Reward(name="Test Reward", description="This is a test for a basic insert", point_cost=100)
    reward.upsert()
    assert reward.id > 0