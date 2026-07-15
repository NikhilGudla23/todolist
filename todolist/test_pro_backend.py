import os
import shutil
import sys
from unittest.mock import patch

# Mock Streamlit session state for testing outside Streamlit runtime
class MockSessionState(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
    def __setattr__(self, name, value):
        self[name] = value

mock_state = MockSessionState()
mock_state.logged_in = False
mock_state.user_id = None
mock_state.username = None
mock_state.user_name = None
mock_state.user_email = None
mock_state.user_created_at = None
mock_state.theme = "Dark"

import utils.database as db
import utils.auth as auth
import utils.validation as val
import utils.search as search
import utils.filter as filter
import utils.sort as sort

def run_tests():
    has_backup = False
    if os.path.exists("database"):
        shutil.move("database", "database_backup")
        has_backup = True
        
    # Patch st.session_state in all loaded modules
    with patch("utils.session.st.session_state", mock_state), \
         patch("utils.auth.sess.st.session_state", mock_state), \
         patch("streamlit.session_state", mock_state):
         
        try:
            db.ensure_store()
            
            # 1. Validation
            assert val.validate_email("test@domain.com")
            assert not val.validate_email("invalid-email")
            assert val.validate_username("user_1")
            assert not val.validate_username("us") # too short
            assert val.validate_password("pass")
            assert not val.validate_password("12") # too short
            
            # 2. Registration and bcrypt hashing
            success, msg = auth.register_user("Test User", "test_user", "test@domain.com", "password", "password")
            assert success, f"Register fail: {msg}"
            
            success, msg = auth.register_user("Test User 2", "test_user", "another@domain.com", "password", "password")
            assert not success, "Should fail: duplicate username"
            
            # 3. Login Setup and Mock Session State validation
            assert auth.login_user("test_user", "password")
            assert mock_state.logged_in
            assert mock_state.username == "test_user"
            
            # 4. JSON read/write and task insertion
            tasks = db.read_json(db.TASKS_FILE)
            assert len(tasks) == 0
            
            user_id = mock_state.user_id
            
            task1 = {
                "id": "t1", "user_id": user_id, "title": "Buy groceries",
                "priority": "Low", "category": "Shopping", "status": "pending", "due_date": "2026-07-20", "duration": 20
            }
            task2 = {
                "id": "t2", "user_id": user_id, "title": "Finish report",
                "priority": "High", "category": "Work", "status": "pending", "due_date": "2026-07-16", "duration": 45
            }
            
            tasks.extend([task1, task2])
            db.write_json(db.TASKS_FILE, tasks)
            
            tasks_loaded = db.read_json(db.TASKS_FILE)
            assert len(tasks_loaded) == 2
            
            # Verify backlog workload calculations
            backlog_sum = sum(int(t.get("duration", 0)) for t in tasks_loaded if t.get("status") == "pending")
            assert backlog_sum == 65, f"Expected workload backlog of 65 minutes, got: {backlog_sum}"
            
            # 5. Search
            res = search.search_tasks(tasks_loaded, "report")
            assert len(res) == 1
            assert res[0]["title"] == "Finish report"
            
            # 6. Filter
            res = filter.filter_tasks(tasks_loaded, priority="High")
            assert len(res) == 1
            assert res[0]["id"] == "t2"
            
            # 7. Sort
            res = sort.sort_tasks(tasks_loaded, "Alphabetical")
            assert res[0]["title"] == "Buy groceries"
            
            # 8. AI Recommendations Heuristics Checks
            from utils.ai import suggest_task_meta
            cat, pri = suggest_task_meta("Buy groceries")
            assert cat == "Shopping" and pri == "Low", f"AI suggest failed for 'Buy groceries': {cat}, {pri}"
            
            cat, pri = suggest_task_meta("Prepare urgent slides for board meeting")
            assert cat == "Work" and pri == "High", f"AI suggest failed for 'Prepare urgent slides...': {cat}, {pri}"
            
            # 9. User Level Mapping Checks
            from utils.helpers import get_user_level, get_relative_due_date
            level, code = get_user_level(0)
            assert code == "Lv.0"
            level, code = get_user_level(10)
            assert code == "Lv.2"
            
            # 10. Relative Due Date Tag Checks
            from datetime import date
            today_str = date.today().strftime("%Y-%m-%d")
            rel = get_relative_due_date(today_str)
            assert "Due Today" in rel, f"Relative due date check failed: {rel}"
            
            print("ALL TASKFLOW PRO BACKEND TESTS PASSED!")
        finally:
            # Restore backup if any
            if os.path.exists("database"):
                shutil.rmtree("database")
            if has_backup:
                shutil.move("database_backup", "database")

if __name__ == "__main__":
    run_tests()
