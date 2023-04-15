package com.bdma.cargo.model;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class GasModel {

    String currency;
    String lpg;
    String diesel;
    String gasoline;
    String country;

}
