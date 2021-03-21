import pandas as pd

projects = [
    {
        'name': 'Project 1',
        'id': 'p1234',
        'owner': {
            'name': 'Ajit',
            'user_id': 'ajit.jadhav@technocrunch.com'
        }
    },
    {
        'name': 'Project 2',
        'id': 'p2234',
        'owner': {
            'name': 'Ajit',
            'user_id': 'ajit.jadhav@technocrunch.com'
        }
    }
]

def get_project(project_id = None):
    if not project_id:
        return None, 'No project ID given'
    try:
        df = pd.DataFrame(projects)
        project = df[df['id'] == project_id]
        project = project.to_dict('records')
        return project, None
    except Exception as error:
        return None, str(error)
