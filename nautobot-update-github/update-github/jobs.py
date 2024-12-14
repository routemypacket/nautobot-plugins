1: from nautobot.extras.jobs import Job
 2: import git
 3: import os
 4: import shutil
 5: import logging
 6: import datetime
 7:
 8: logger = logging.getLogger(__name__)
 9:
10: class UpdateGitHub(Job):
11:     """Updates the GitHub repository with configuration changes."""
12:
13:     class Meta:
14:         name = "Update GitHub Repository"
15:         description = "Commits and pushes config changes to GitHub."
16:         read_only = False
17:         commit_default = True
18:
19:     def run(self, data, commit):
20:         # *** CRITICAL: How you handle credentials ***
21:         username = os.environ.get("GIT_USERNAME")
22:         token = os.environ.get("GIT_TOKEN")
23:         repo_owner = os.environ.get("GIT_REPO_OWNER")
24:         repo_name = os.environ.get("GIT_REPO_NAME")

25:         if not all([username, token, repo_owner, repo_name]):
26:             raise Exception("GIT_USERNAME, GIT_TOKEN, GIT_REPO_OWNER and GIT_REPO_NAME environment variables must be set")

27:         repo_url = f"https://{username}:{token}@github.com/{repo_owner}/{repo_name}.git"
28:
29:         # The rest of this can be customized as needed, but the defaults are usually fine.
30:         repo_path = "/tmp/config_repo"
31:         branch_name = "main"
32:         device_name = data.get("device_name", "default_device")
33:         config_data = data.get("config_data", f"config updated at {datetime.datetime.now()}")
34:         config_file_path = data.get("config_file_path", "configs/routers")
35:
36:         try:
37:             if os.path.exists(repo_path):
38:                 shutil.rmtree(repo_path)
39:
40:             repo = git.Repo.clone_from(repo_url, repo_path)
41:             repo.git.checkout(branch_name)
42:
43:             config_file = os.path.join(repo_path, config_file_path, f"{device_name}.yaml")
44:             os.makedirs(os.path.dirname(config_file), exist_ok=True)
45:             with open(config_file, "w") as f:
46:                 f.write(config_data)
47:
48:             if repo.is_dirty(untracked_files=True):
49:                 repo.git.add(config_file)
50:                 repo.git.commit("-m", f"Automated update from Nautobot: Updated config for {device_name}")
51:                 origin = repo.remote(name="origin")
52:                 origin.push()
53:                 self.log_success(f"Git repository updated successfully for {device_name}.")
54:             else:
55:                 self.log_info("No changes to commit.")
56:
57:         except git.GitCommandError as e:
58:             self.log_error(f"Git error: {e}")
59:             raise
60:         except Exception as e:
61:             self.log_error(f"An unexpected error occurred: {e}")
62:             raise
63:         finally:
64:             if os.path.exists(repo_path):
65:                 shutil.rmtree(repo_path)