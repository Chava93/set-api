import numpy as np


class TransformRequest:
    """
    Transofrmar consultar a listas
    """
    attributes = {
    "forma":('churro', 'ovalo', 'rombo'),
    "numero": ('dos', 'tres', 'uno'),
    "color":('morado', 'rojo', 'verde'),
    "relleno":('blanco', 'rayado', 'solido')
    }
    handler = [1,0,0],[0,1,0],[0,0,1]
    def Single_card(attrs):
        """
        Transofrmar una sola carta
        Input:
            attrs: dict
                with keys: ("forma","numero","color","relleno")
        Returns:
            list
                where len(list)==12
        """
        ind = [TransformRequest.attributes[k].index(v) for k,v in attrs.items()]
        return [n for i in ind for n in TransformRequest.handler[i]]
    def DeckToList(deck):
        """
        Transformar una lista de diccionarios

        """
        return [TransformRequest.Single_card(card) for card in deck]

class SetModel(TransformRequest):
    def findSets(X):
        """
        Function that given an array of cards find sets.
        Input:
            X: np.array
                Array de cartas en el tablero donde
                X.shape = (n_cartas,n_features)
                Por definición del juego n_features simempre es igual a 12
        Output:
            R: tuple de np.arrays
                Cada tuple se lee de manera vertical y representa el índice
                de las cartas ganadores. Este indice es la representacion de enumerar
                las cartas de 0 a n cartas.
        """
        n_cards = X.shape[0]
        # Expandir Matriz
        X2 = X.reshape((n_cards,1,12))
        # Primera comparacion
        # Encontramos coincidencias 2 a 2
        X3 = X2 + X
        ## Nuevamente expandimos
        X4 = X3.reshape((n_cards,n_cards,1,12))
        ## Comparacion 3 a 3
        X4 =  X4 + X
        ## Creamos matriz filtro
        ## Esta matriz nos indica los conjuntos
        ## donde dos condiciones son igues y una no
        X5 = (X4==2).sum(axis=3)
        # Estos son los índices ganadores!
        # Los índices donde no hay 2
        R = (X5==0).nonzero()
        return R
    def prune_results(results):
        """
        Once we found the winner indices
        remove diagonal and remove duplicates
        Input
        ------
            results: tuple of arrays
                representing the indices of the cards that are a "set"
        Output
        ------
            res: np.array
                where each row represent the index of a "set" card
        """
        res = np.array(results)
        ## Remove duplicates
        ## (i.e. mean(column)!= max(column))
            # Find non-equal column indices
        non_equal = np.apply_along_axis(lambda col: max(col)!=np.mean(col),0,res)
            # Select non equal columns
        res= res[:, non_equal]
        ## remove duplicates
            ## Sort values and transpose
        res = np.apply_along_axis(sorted,0,res).T
            ## Get unique values
        res = np.unique(res,axis=0)
        return res
    def Solve(X):
        """
        Input:
            X: np.array
                Array de cartas en el tablero donde
                X.shape = (n_cartas,n_features)
                Por definición del juego n_features simempre es igual a 12
        Output
        ------
            res: np.array
                where each row represent the index of a "set" card

        """
        ## Aplicar modelo
        gan = SetModel.findSets(X)
        ## Limpiar indices
        results = SetModel.prune_results(gan)
        return results
    def SolveFromRequest(request):
        """
        Convertir request a un np.array y de ahí aplicar el modelo.
        Input
        -----
            request: list
                lista de diccionarios
         Output
        ------
            res: np.array
                where each row represent the index of a "set" card
        """
        X = TransformRequest.DeckToList(request)
        X = SetModel.Solve(np.array(X))
        return X.tolist()
