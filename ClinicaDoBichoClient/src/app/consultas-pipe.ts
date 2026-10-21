import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'consultas',
})
export class ConsultasPipe implements PipeTransform {
  transform(value: unknown, ...args: unknown[]): unknown {
    return null;
  }
}
