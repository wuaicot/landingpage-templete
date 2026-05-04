import React from "react";

export const Services = (props) => {
  return (
    <section id="services" className="text-center">
      <div className="container">
        <div className="section-title">
          <h2>Servicios de Desarrollo de Software de Alto Nivel</h2>
          <p>
            Soluciones integrales de desarrollo web diseñadas para escalar su negocio y dominar el mercado digital.
          </p>
        </div>
        <div className="row">
          {props.data
            ? props.data.map((d, i) => (
                <div key={`${d.name}-${i}`} className="col-md-4">
                  {" "}
                  <i className={d.icon}></i>
                  <div className="service-desc">
                    <h3>{d.name}</h3>
                    <p>{d.text}</p>
                  </div>
                </div>
              ))
            : "loading"}
        </div>
      </div>
    </section>
  );
};
