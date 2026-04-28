import React from "react";

export const Team = (props) => {
  return (
    <div id="team" className="text-center">
      <div className="container">
        <div className="col-md-8 col-md-offset-2 section-title">
          <h2>Nuestro Equipo</h2>
          <p>
            Profesionales comprometidos con la excelencia técnica y la innovación constante en cada proyecto.
          </p>
        </div>
        <div className="row">
          {props.data
            ? props.data.map((d, i) => (
                <div key={`${d.name}-${i}`} className="col-lg-3 col-md-6 col-sm-6">
                  <div className="thumbnail">
                    {" "}
                    <img src={d.img} alt={`Naycol Linares Team - ${d.name} - ${d.job}`} className="team-img" />
                    <div className="caption">
                      <h4>{d.name}</h4>
                      <p>{d.job}</p>
                    </div>
                  </div>
                </div>
              ))
            : "cargando..."}
        </div>
      </div>
    </div>
  );
};
