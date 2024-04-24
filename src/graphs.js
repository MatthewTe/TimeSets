export class Graph {
    adjacencyList;

    constructor() {
        this.adjacencyList = new Map();
    }

    addNode(node) {
        this.adjacencyList.set(node, new Map())
    }

    addEdge(node1, node2, weight) {
        this.adjacencyList.get(node1).set(node2, weight);
        this.adjacencyList.get(node2).set(node1, weight)
    }

    getNeighboors(node) {
        return this.adjacencyList.get(node)
    }

    doesNodeExist(node) {
        return (!this.adjacencyList.get(node) === null)
    }

    getNode(node) {
        return this.adjacencyList.get(node)
    }

}
