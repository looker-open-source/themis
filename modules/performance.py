import json
from typing import Tuple, List
from collections import Counter
from looker_sdk.sdk.api40 import methods
from looker_sdk.sdk.api40 import models


class Performance:
	
	
	def __repr__(self) -> str:
		return 'PERFORMANCE IN LOOKER'
	
	def __init__(self, looker_client: methods.Looker40SDK) -> None:
		self.looker_client = looker_client

	def unlimited_downloads(self) -> Tuple[str, str]:
		"""Returns unlimited downloads information from instance.

		Returns:
			results: The summary of unlimited results from query.
			unltd_downloads.share_url: The link to access result in Looker.
		"""
		body = models.WriteQuery(
			model = "system__activity",
			view = "history",
			fields = [
				"history.created_time",
				"query.link",
				"user.id",
				"user.name",
				"history.source",
				"query.limit"
			],
			filters = {
					"history.created_time": "24 hours",
					"history.source": "-regenerator,-suggest",
					"query.limit": ">5000"
			},
			sorts = ["history.created_time desc"],
			limit = "500"
		)
		unltd_downloads = self.looker_client.create_query(body)
		unlimited_downloads = self.looker_client.run_query(unltd_downloads.id, 
																										result_format='json'
																										)
		if unlimited_downloads:
			unltd_source = [
				query['history.source'] for query in json.loads(unlimited_downloads)
			]

			unltd_users = [
				query['user.id'] for query in json.loads(unlimited_downloads)
			]
			
			results = "{} users have ran queries with more than 5000 rows \
								from these sources: {}".format(
												len(list(set(unltd_users))), 
												list(set(unltd_source))
												)
			return results, unltd_downloads.share_url
		else:
			return None, unltd_downloads.share_url

	def check_if_clustered(self) -> bool:
		"""Checks if Looker is using a clustered settup.

		Returns:
			A boolean value representing whether the instance is clustered.
		"""
		body = models.WriteQuery(
			model = "system__activity",
			view = "history",
			fields = ["node.clustered", "node.mac_adress","node.count"],
			filters = {"node.mac_adress": "-null"},
			sorts = ["node.count desc"],
			limit = "500"
		)
		cluster_check = self.looker_client.create_query(body)
		check_clustered = self.looker_client.run_query(cluster_check.id, 
																									result_format='json'
																									)
		nodes_count = len(json.loads(check_clustered))

		node_is_cluster = [
				node['node.clustered'] for node in json.loads(check_clustered)
			]

		return nodes_count > 1 and list(set(node_is_cluster))[0] == "Yes"

	def nodes_matching(self) -> List[str]:
		"""For clusters, checks if the nodes are on same Looker version.

		Returns:
			diff_node_version: The list with information aobut nodes and versions.
		"""
		body = models.WriteQuery(
			model = "system__activity",
			view = "history",
			fields = [
				"node.id",
				"node.version",
				"node.last_heartbeat_time",
				"node.last_heartbeat_time"
			],
			filters = {
				"node.last_heartbeat_date": "1 days"
			},
			sorts = ["node.last_heartbeat_time desc"],
			limit = "500",
			vis_config = {
				"hidden_fields": ["node.id","node.version","node.last_heartbeat_time","most_recent_heartbeat","node.count"]
			},
 			dynamic_fields = "[{\"table_calculation\":\"most_recent_heartbeat\",\"label\":\"most_recent_heartbeat\",\"expression\":\"diff_minutes(${node.last_heartbeat_time}, now())\",\"value_format\":null,\"value_format_name\":null,\"_kind_hint\":\"dimension\",\"_type_hint\":\"number\"},{\"table_calculation\":\"node_version_at_last_beat\",\"label\":\"node_version_at_last_beat\",\"expression\":\"if(diff_minutes(${node.last_heartbeat_time}, now())  > ${most_recent_heartbeat}*1.10 OR diff_minutes(${node.last_heartbeat_time}, now()) < ${most_recent_heartbeat}*0.90, ${node.version}, null)\",\"value_format\":null,\"value_format_name\":null,\"_kind_hint\":\"dimension\",\"_type_hint\":\"string\"}]"		)
		node_check = self.looker_client.create_query(body)
		nodes_versions = self.looker_client.run_query(node_check.id, result_format='json')
		
		# to exclude older heartbeat checks with None values
		results = [
          version for version in json.loads(nodes_versions) 
					if version['node_version_at_last_beat']
      ]

		diff_node_version = []
		if len(list(set(results))) == 1:
			diff_node_version.append("All {} Nodes found on same Looker version".format(
					len(results))
					)
			return diff_node_version
		else:	
			for k,v in Counter(results).items():
				diff_node_version.append("{} nodes found on version {}".format(v,k))
			return diff_node_version
