#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <vector>
#include <list>
#include <map>
#include <locale>
#include <windows.h>

using namespace std;

class Graph {
private:
	map<string, map<string, int>> AdjList;
	bool direct;
	bool weight;

public:
	Graph(map<string, map<string, int>> a, bool d, bool w) {
		AdjList = a;
		direct = d;
		weight = w;
	}

	Graph(const Graph &g) {
		this->AdjList = g.AdjList;
		this->direct = g.direct;
		this->weight = g.weight;
	}

	void operator()(const Graph &g) {
		this->AdjList = g.AdjList;  
		this->direct = g.direct;  
		this->weight = g.weight;
	}

	Graph() {
		AdjList.clear();
		direct = false;
		weight = 0;
	}

	~Graph() {
		direct = false;
		weight = false;
		AdjList.clear();
	}

	bool GetDir() {
		return this->direct;
	}

	bool GetWeight() {
		return this->weight;
	}

	void SetDir(bool d) {
		this->direct = d;
	}

	void SetWeight(bool w) {
		this->weight = w;
	}

	bool ExistVertex(string v) {
		return AdjList.find(v) != AdjList.end();
	}

	bool ExistEdge(string v1, string v2) {
		return AdjList.find(v1)->second.find(v2) != AdjList.find(v1)->second.end();
	}

	map <string, map<string, int>> GetAdj() {
		return this->AdjList;
	}

	void AddVertex(string v) {
		if (!ExistVertex(v)) {
			map<string, int> second;
			AdjList.insert({ v, second });
		}
		else {
			cout << "Вершина уже существует" << endl;
		}
	}

	void AddEdge(string v1, string v2) {   //для невзвешенного
		if (!ExistVertex(v1) || !ExistVertex(v2)) {
			cout << "Вершин не существует\n";
		}
		else {
			if (ExistEdge(v1, v2)) {
				cout << "Ребро уже существует!\n";
			}
			else {
				AdjList[v1][v2];
				if (!direct) {
					AdjList[v2][v1];
				}
			}
		}
	}

	void AddEdge(string v1, string v2, int w) { //для взвешенного
		if (!ExistVertex(v1) || !ExistVertex(v2)) {
			cout << "Вершин не существует\n";
		}
		else {
			if (ExistEdge(v1, v2)) {
				cout << "Ребро уже существует!\n";
			}
			else {
				AdjList[v1][v2] = w;
				if (!direct) {
					AdjList[v2][v1] = w;
				}
			}
		}
	}

	void DeleteVertex(string v) {
		if (ExistVertex(v) == false) {
			cout << "Вершины не существует\n";
		}
		else {
			for (auto& it : AdjList) {
				if (it.second.find(v) != it.second.end()) {
					it.second.erase(v);
				}
			}
			AdjList.erase(v);
		}
	}

	void DeleteEdge(string v1, string v2) {
		if (ExistEdge(v1, v2)) {
			map<string, map<string, int>>::iterator i;
			map<string, int>::iterator j;

			i = AdjList.find(v1);
			j = i->second.find(v2);
			i->second.erase(j);
			if (!direct) {
				AdjList.find(v2)->second.erase(v1);
			}
		}
		else {
			cout << "Ребра не существует\n";
		}
	}

	void PrintList() {
		if (weight) {
			for (auto& elem : AdjList) {
				cout << "vertex " << elem.first + ": ";
				for (auto& it : elem.second) {
					cout << it.first << " (w = " << it.second << "); ";
				}
				cout << "\n";
			}
			cout << "\n";
		}
		else {
			for (auto& elem : AdjList) {
				cout << "vertex " << elem.first + ": ";
				for (auto& it : elem.second) {
					cout << it.first << "; ";
				}
				cout << "\n";
			}
			cout << "\n";
		}
	}

	void loadFromFile(string filename) {
		ifstream in(filename);
		if (!in.is_open()) {
			throw runtime_error("Не удалось открыть файл для чтения.");
		}
		string dir;
		in >> dir;
		if (dir == "directed") {
			direct = true;
		}
		else if (dir == "undirected") {
			direct = false;
		}
		else {
			throw runtime_error("Неверный формат файла: не указано directed или undirected\n");
		}

		string type;
		in >> type;
		if (type == "weighted") {
			weight = true;
		}
		else if (type == "unweighted") {
			weight = false;
		}
		else {
			throw runtime_error("Неверный формат файла: не указано weighted или unweighted\n");
		}

		if (weight) {
			string u, v;
			int weight;
			while (in >> u >> v >> weight) {
				if (!ExistVertex(u)) {
					AddVertex(u);
				}
				if (!ExistVertex(v)) {
					AddVertex(v);
				}
				AddEdge(u, v, weight);
			}
		}
		else {
			string u, v;
			while (in >> u >> v) {
				if (!ExistVertex(u)) {
					AddVertex(u);
				}
				if (!ExistVertex(v)) {
					AddVertex(v);
				}
				AddEdge(u, v);
			}
		}
	}

	void Task2() {
		map<string, int> outDegrees; // Полустепень исхода
		map<string, int> inDegrees;  // Полустепень захода

		for (auto vertex : AdjList) {
			outDegrees[vertex.first] = 0;
			inDegrees[vertex.first] = 0;
		}

		for (auto vertex : AdjList) {
			string v1 = vertex.first;
			for (auto edge : vertex.second) {
				string v2 = edge.first;
				outDegrees[v1]++;
				inDegrees[v2]++;
			}
		}

		cout << "Вершины с полустепенью исхода больше полустепени захода:\n";
		for (auto vertex : outDegrees) {
			string v = vertex.first;
			if (outDegrees[v] > inDegrees[v]) {
				cout << "Вершина " << v << " (" << outDegrees[v] << ", " << inDegrees[v] << ")\n";
			}
		}

		cout << "\n";
	}

	//void Task3(string v) {
	//	map<string, int> outV; // Полустепень исхода
	//	map<string, int> inV;  // Полустепень захода

	//	for (auto vertex : AdjList) {
	//		outV[vertex.first] = 0;
	//		inV[vertex.first] = 0;
	//	}

	//	for (auto vertex : AdjList) {
	//		string v1 = vertex.first;
	//		for (auto edge : vertex.second) {
	//			string v2 = edge.first;
	//			outV[v1]++;
	//			inV[v2]++;
	//		}
	//	}

	//	for (auto vertex : AdjList[v]) {
	//		if (AdjList[vertex] != 0) {

	//		}
	//	}
	//}

};