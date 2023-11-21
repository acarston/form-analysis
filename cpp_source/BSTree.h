#ifndef BSTREE_H
#define BSTREE_H

#include <cmath>
#include <stack>
#include <string>
#include <fstream>

template <typename T>
class BSTree {
private:
	template <typename U>
	struct Node {
		U info;
		Node* left = nullptr;
		Node* right = nullptr;
		int height = 1;

		Node(U info) : info(info) {};
	};

	Node<T>* root = nullptr;

	bool set_root(T& rootVal) {
		if (root == nullptr) {
			root = new Node<T>(rootVal);
			return true;
		}
		return false;
	};

	int get_height(Node<T>* node) {
		if (node == nullptr) return 0;
		else return node->height;
	};

	// calculate a subtree height
	// defined as the largest height of its subtrees plus 1
	void set_height(Node<T>* node) {
		node->height = 1 + (std::max)(get_height(node->right), get_height(node->left));
	};

	// calculate the balance factor based on node subtree heights
	int get_balfactor(Node<T>* node) {
		return get_height(node->right) - get_height(node->left);
	};

	Node<T>* rotate_left(Node<T>* p, Node<T>* ch) {
		p->right = ch->left;
		ch->left = p;

		set_height(p);
		set_height(ch);

		return ch;
	};

	Node<T>* rotate_right(Node<T>* p, Node<T>* ch) {
		p->left = ch->right;
		ch->right = p;

		set_height(p);
		set_height(ch);

		return ch;
	};

	Node<T>* rotate_leftright(Node<T>* p, Node<T>* ch) {
		p->left = rotate_left(ch, ch->right);
		return rotate_right(p, p->left);
	};

	Node<T>* rotate_rightleft(Node<T>* p, Node<T>* ch) {
		p->right = rotate_right(ch, ch->left);
		return rotate_left(p, p->right);
	};

	// perform rotations along the insert path
	void balance(std::stack<Node<T>*>& path) {
		while (true) {
			Node<T>* cur = path.top();
			// update subtree heights along the path
			set_height(cur);
			path.pop();

			// if cur is root
			if (path.empty()) break;

			Node<T>* par = path.top();
			int parBalFactor = get_balfactor(par);
			int curBalFactor = get_balfactor(cur);

			// get the grandparent without modifying the stack
			path.pop();
			Node<T>* gr = path.empty() ? nullptr : path.top();
			path.push(par);

			// perform a rotation according to balance factors
			Node<T>* newPar;
			if (parBalFactor > 1) {
				if (curBalFactor > 0) newPar = rotate_left(par, cur);
				else newPar = rotate_rightleft(par, cur);
			}
			else if (parBalFactor < -1) {
				if (curBalFactor < 0) newPar = rotate_right(par, cur);
				else newPar = rotate_leftright(par, cur);
			}
			else continue;

			// make grandparent point to the new subtree root
			if (gr == nullptr) {
				// the new subtree root was the tree root
				root = newPar;
			}
			else {
				if (gr->right == par) gr->right = newPar;
				else gr->left = newPar;
			}

			// remove the old parent from the stack
			path.pop();
			if (path.empty()) break;
		}
	};

public:
	BSTree() {};
	BSTree(T rootVal) { root = new Node<T>(rootVal); };

	// make an insertion with AVL self-balancing
	// implementation is original; everything is managed by a stack
	// which keeps track of the path taken by the new insert
	void insert(T val, void (*on_duplicate)(T& current, T& incoming) = nullptr) {
		if (set_root(val)) return;

		std::stack<Node<T>*> path;
		Node<T>* p = root;
		path.push(p);
		while (true) {
			if (val > p->info) {
				if (p->right == nullptr) {
					p->right = new Node<T>(val);
					if (p->left == nullptr) break;
					// balance only if the tree has been skewed
					else return;
				}
				p = p->right;
			}
			else if (val < p->info) {
				if (p->left == nullptr) {
					p->left = new Node<T>(val);
					if (p->right == nullptr) break;
					else return;
				}
				p = p->left;
			}
			else {
				// skip duplicates if no handling is passed in
				if (on_duplicate != nullptr) on_duplicate(p->info, val);
				return;
			}
			path.push(p);
		}

		balance(path);
	};

	// insert with custom comparison values
	template <typename U>
	void insert(T val, U& (*get_member)(T& info), void (*on_duplicate)(T& current, T& incoming) = nullptr) {
		if (set_root(val)) return;

		std::stack<Node<T>*> path;
		Node<T>* p = root;
		path.push(p);
		while (true) {
			if (get_member(val) > get_member(p->info)) {
				if (p->right == nullptr) {
					p->right = new Node<T>(val);
					if (p->left == nullptr) break;
					else return;
				}
				p = p->right;
			}
			else if (get_member(val) < get_member(p->info)) {
				if (p->left == nullptr) {
					p->left = new Node<T>(val);
					if (p->right == nullptr) break;
					else return;
				}
				p = p->left;
			}
			else {
				if (on_duplicate != nullptr) on_duplicate(p->info, val);
				return;
			}
			path.push(p);
		}

		balance(path);
	};

	// insert with custom comparison function
	// requires duplicate handling
	void insert(T val, int (*compare)(T& current, T& incoming), void (*on_duplicate)(T& current, T& incoming)) {
		if (set_root(val)) return;

		std::stack<Node<T>*> path;
		Node<T>* p = root;
		path.push(p);
		while (true) {
			if (compare(p->info, val) > 0) {
				if (p->right == nullptr) {
					p->right = new Node<T>(val);
					if (p->left == nullptr) break;
					else return;
				}
				p = p->right;
			}
			else if (compare(p->info, val) < 0) {
				if (p->left == nullptr) {
					p->left = new Node<T>(val);
					if (p->right == nullptr) break;
					else return;
				}
				p = p->left;
			}
			else {
				on_duplicate(p->info, val);
				return;
			}
			path.push(p);
		}

		balance(path);
	};

	// Morris inorder traversal algorithm. adapted from 
	// https://takeuforward.org/data-structure/morris-inorder-traversal-of-a-binary-tree/
	void traverse_inorder(void (*visit)(T& info)) {
		Node<T>* cur = root;
		while (cur != nullptr) {
			// visit, move to the right if no left child
			if (cur->left == nullptr) {
				visit(cur->info);
				cur = cur->right;
			}
			else {
				// look for the rightmost subtree node
				Node<T>* p = cur->left;
				while (true) {
					// make current the right child of this node
					// point current to the new 'root'
					if (p->right == nullptr) {
						p->right = cur;
						cur = cur->left;
						break;
					}
					// remove the new connection
					// visit, move to the right
					if (p->right == cur) {
						p->right = nullptr;
						visit(cur->info);
						cur = cur->right;
						break;
					}
					p = p->right;
				}
			}
		}
	};

	// traverse and visit with an output file
	void traverse_inorder(void (*visit)(T& info, std::ofstream& f), const std::string& filePath) {
		Node<T>* cur = root;
		std::ofstream fout(filePath);
		while (cur != nullptr) {
			if (cur->left == nullptr) {
				visit(cur->info, fout);
				cur = cur->right;
			}
			else {
				Node<T>* p = cur->left;
				while (true) {
					if (p->right == nullptr) {
						p->right = cur;
						cur = cur->left;
						break;
					}
					if (p->right == cur) {
						p->right = nullptr;
						visit(cur->info, fout);
						cur = cur->right;
						break;
					}
					p = p->right;
				}
			}
		}
	};
};

#endif