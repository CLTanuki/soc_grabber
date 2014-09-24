__author__ = 'cltanuki'
from TwitterAPI import TwitterAPI

api = TwitterAPI('65dxiPhn10SE3zJT6fVEPWsVx', 'VmK0rQFapjymwtSNpidi0Yfe16mjMdHXBhZTmYVc8dwb1joAxX',
                 '109566527-ZufkixJ3XInW91ZE34hGFtxQcrXGOzBS7vBdApUP', '0N5poNnJoDsWO8Yvf1FfNECfOJKJm7nKthPVzow7apyPu')

r = api.request('users/lookup', {'screen_name':'mfoxru'})
for item in r.get_iterator():
    for k, v in item.items():
        print(k)