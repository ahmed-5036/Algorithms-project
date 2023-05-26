import csv
import json
import matplotlib.pyplot as plt
import networkx as nx
import snscrape.modules.twitter as sntwitter

# Function to scrape tweets
def scrape_tweets(username, count):
    tweets = []
    for tweet in sntwitter.TwitterUserScraper(username).get_items():
        if len(tweets) >= count:
            break
        tweets.append(tweet)
    return tweets

# Function to perform network analysis
def perform_network_analysis(graph):
    # Connected graph
    connected_graph = max(nx.connected_components(graph), key=len)
    connected_graph = graph.subgraph(connected_graph)

    # Network analysis
    degree_centrality = nx.degree_centrality(connected_graph)
    betweenness_centrality = nx.betweenness_centrality(connected_graph)
    closeness_centrality = nx.closeness_centrality(connected_graph)
    eigenvector_centrality = nx.eigenvector_centrality(connected_graph)
    clustering_coefficients = nx.clustering(connected_graph)
    density = nx.density(connected_graph)
    network_type = nx.is_directed(connected_graph)

    # Visualization of Betweenness Centrality
    plt.figure(figsize=(6, 4))
    plt.bar(range(len(betweenness_centrality)), list(betweenness_centrality.values()), align='center')
    plt.xticks(range(len(betweenness_centrality)), list(betweenness_centrality.keys()), rotation='vertical')
    plt.xlabel('Nodes')
    plt.ylabel('Betweenness Centrality')
    plt.title('Betweenness Centrality')
    plt.tight_layout()
    plt.show()

    # Visualization of Degree Centrality
    plt.figure(figsize=(6, 4))
    plt.bar(range(len(degree_centrality)), list(degree_centrality.values()), align='center')
    plt.xticks(range(len(degree_centrality)), list(degree_centrality.keys()), rotation='vertical')
    plt.xlabel('Nodes')
    plt.ylabel('Degree Centrality')
    plt.title('Degree Centrality')
    plt.tight_layout()
    plt.show()

    # Print or save the analysis results as needed
    print("Degree Centrality:", degree_centrality)
    print("Betweenness Centrality:", betweenness_centrality)
    print("Closeness Centrality:", closeness_centrality)
    print("Eigenvector Centrality:", eigenvector_centrality)
    print("Clustering Coefficients:", clustering_coefficients)
    print("Density:", density)
    print("Network Type:", network_type)

    # Store nodes and edges in CSV
    with open('nodes.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Node', 'Degree Centrality', 'Betweenness Centrality', 'Closeness Centrality',
                         'Eigenvector Centrality', 'Clustering Coefficient'])
        for node in connected_graph.nodes():
            writer.writerow([
                node,
                degree_centrality.get(node, 0),
                betweenness_centrality.get(node, 0),
                closeness_centrality.get(node, 0),
                eigenvector_centrality.get(node, 0),
                clustering_coefficients.get(node, 0)
            ])

    with open('edges.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Source', 'Target'])
        for edge in connected_graph.edges():
            writer.writerow(edge)

    # Store nodes and edges in JSON
    nodes_data = []
    for node in connected_graph.nodes():
        nodes_data.append({
            'id': node,
            'degree_centrality': degree_centrality.get(node, 0),
            'betweenness_centrality': betweenness_centrality.get(node, 0),
            'closeness_centrality': closeness_centrality.get(node, 0),
            'eigenvector_centrality': eigenvector_centrality.get(node, 0),
            'clustering_coefficient': clustering_coefficients.get(node, 0)
        })

    edges_data = []
    for edge in connected_graph.edges():
        edges_data.append({
            'source': edge[0],
            'target': edge[1]
        })

    with open('nodes.json', 'w') as f:
        json.dump(nodes_data, f, indent=4)

    with open('edges.json', 'w') as f:
        json.dump(edges_data, f, indent=4)

    # Visualization of the Network Graph
    nx.draw(connected_graph, with_labels=True)
    plt.show()

# Main function
def main():
    # Scrape tweets
    username = input("Enter the Twitter username: ")
    count = int(input("Enter the number of tweets to scrape: "))

    print("Scraping tweets...")
    tweets = scrape_tweets(username, count)
    print("Scraping completed.")

    # Create a graph
    graph = nx.Graph()

    # Add nodes and edges to the graph
    for tweet in tweets:
        user_id = tweet.user.id
        graph.add_node(user_id)

        mentioned_users = [mention.split('@')[1] for mention in tweet.rawContent.split() if mention.startswith('@')]
        for mention in mentioned_users:
            mention_id = mention
            graph.add_node(mention_id)
            graph.add_edge(user_id, mention_id)

    # Perform network analysis
    perform_network_analysis(graph)

if __name__ == '__main__':
    main()

