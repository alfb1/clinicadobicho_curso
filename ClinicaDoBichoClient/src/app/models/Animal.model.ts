import {Dono} from "./Dono.model";

export interface Animal{
            id?: number;
            nome: string;
            especie: string;
            especie_nome: string;
            raca: string;
            idade: string;
            peso: string;
            doneo: Dono;
        }