class BinaryTreeNode:

  def __init__(self, data):
    self.data = data
    self.leftchild = None
    self.rightchild = None


  def __str__(self, level=0):
    ret = "  " *level + str(self.data) + "\n"
    if self.leftchild:
       ret += self.leftchild.__str__(level+1)
    if self.rightchild:
       ret += self.rightchild.__str__(level+1)
    return ret


def printTree(Node, prefix="", is_left=True):
    if not Node:
        return

    if Node.rightchild:
        printTree(Node.rightchild, prefix + ("│    " if is_left else "    "), False)

    print(prefix + ("└── " if is_left else "┌── ") + str(Node.data))

    if Node.leftchild:
        printTree(Node.leftchild, prefix + ("     " if is_left else "│   "), True)


    def Pre_Order(root):

        if root is None:
            return

        print(root.data) #Procesar/Recorro/Visito el nodo actual
        Pre_Order(root.leftchild)
        Pre_Order(root.rightchild)

    def Post_Order(root):

        if root is None:
            return

        Post_Order(root.leftchild)
        Post_Order(root.rightchild)
        print(root.data) #Procesar/Recorro/Visito el nodo actual

    def In_Order(root):

        if root is None:
            return

        In_Order(root.leftchild)
        print(root.data) #Procesar/Recorro/Visito el nodo actual
        In_Order(root.rightchild)
        
        


class Node:
  __slots__ = ('__value','__next')

  def __init__(self,value):
    self.__value = value
    self.__next = None

  def __str__(self):
    return str(self.__value)

  @property
  def next(self):
    return self.__next

  @next.setter
  def next(self,node):
    if node is not None and not isinstance(node,Node):
      raise TypeError("next debe ser un objeto tipo nodo ó None")
    self.__next = node

  @property
  def value(self):
    return self.__value

  @value.setter
  def value(self,newValue):
    if newValue is None:
      raise TypeError("el nuevo valor debe ser diferente de None")
    self.__value = newValue


class LinkedList:

  def __init__(self):
    self.__head = None
    self.__tail = None
    self.__size = 0

  @property
  def head(self):
    return self.__head

  @property
  def tail(self):
    return self.__tail

  @property
  def size(self):
    return self.__size

  @head.setter
  def head(self,node):
    if node is not None and not isinstance(node,Node):
      raise TypeError("Head debe ser un objeto tipo nodo ó None")
    self.__head = node

  @tail.setter
  def tail(self,node):
    if node is not None and not isinstance(node,Node):
      raise TypeError("Tail debe ser un objeto tipo nodo ó None")
    self.__tail = node

  @size.setter
  def size(self,num):
    self.__size = num

  def __str__(self):
    result = [str(nodo.value) for nodo in self]
    return ' <--> '.join(result)

  def print(self):
    for nodo in self:
      print(str(nodo.value))

  def __iter__(self):
    current = self.__head
    while current is not None:
      yield current
      current = current.next

  def append(self,value): # Adicionar al final
    newnode = Node(value)
    if self.__head is None:
      self.__head = newnode
      self.__tail = newnode
    else:
      self.__tail.next = newnode #enlazo nuevo nodo
      self.__tail = newnode
    self.__size += 1


  def popfirst(self):
    tempNode = self.__head
    if self.__head is None:
      return None
    elif self.__size == 1:
      self.__head = None
      self.__tail = None
      self.__size = 0
    else:
      self.__head = self.__head.next
      self.__size -= 1

    tempNode.next = None  #limpiar la referencia al segundo nodo, ahora nueva cabeza
    return tempNode


class Queue:

  def __init__(self):
    self.__queue = LinkedList()


  def enqueue(self, e):
    self.__queue.append(e)
    return True

  def dequeue(self):
    if self.is_empty():
      return "No hay elementos en la cola"
    else:
      first_node = self.__queue.popfirst()
      return first_node.value

  def is_empty(self):
    return  self.__queue.size == 0

  def len(self):
    return  self.__queue.size


  def firs(self):
    return self.__queue.head.value

  def __str__(self):
    result = [str(nodo.value) for nodo in self.__queue]
    return ' -- '.join(result)


def LeverOrder(root):

  if root is None:
    return

  auxQueue = Queue()
  auxQueue.enqueue(root)

  while not auxQueue.is_empty():

    current_root = auxQueue.dequeue()
    print(current_root.data) #Proceso/Imprimo

    if current_root.leftchild:
      auxQueue.enqueue(current_root.leftchild)

    if current_root.rightchild:
      auxQueue.enqueue(current_root.rightchild)


