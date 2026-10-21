import {Animal} from "./Animal.model";
import {Veterinario} from "./Veterinario.model";

export interface Consulta{
    id?:number;
    animal:Animal;
    veterinario:Veterinario;
    data:string;
    motivo:string;
    observacoes?:string;
}