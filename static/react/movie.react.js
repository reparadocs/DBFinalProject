var MovieCell = React.createClass({
  getInitialState: function() {
    return {
      title: "",
      img_url: "",
      movie_id: ""
    };
  },
  _getNewMovie: function() {
    $.ajax({
      url: '/get_movie/' + this.props.user_id + '/' + this.props.rid + '/',
      dataType: 'json',
      success: function(data) {
        this.setState(data);

      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    })
  },
  componentDidMount: function() {
    this._getNewMovie();
  },
  _ratingOnChange: function(rating) {
    $.ajax({
      url: '/rate/' + this.props.user_id + '/' + this.state.movie_id +'/',
      type: 'POST',
      dataType: 'json',
      data: {'rating': rating},
      success: function(data) {
        this._getNewMovie();
        this.props.fetch();
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  render: function() {
    var image_url = this.state.img_url;
    if(!image_url || image_url === "") {
      image_url = "http://i.imdb.com/images/nopicture/140x209/unknown.png";
    }
    return (
      <div>
      <a href={'/movie/' + this.state.movie_id}>
      <h4>{this.state.title}</h4>
      <img style={{height: '268px', width: '182px'}} src={image_url} />
      </a>
<IconRating onChange={this._ratingOnChange}
  toggledClassName="fa-2x fa fa-star " untoggledClassName="fa-2x fa fa-star-o"/>

      </div>
    );
  }

});

var RMovie = React.createClass({
  _ratingOnChange: function(rating) {
    $.ajax({
      url: '/rate/' + this.props.user_id + '/' + this.props.movie.movie_id +'/',
      type: 'POST',
      dataType: 'json',
      data: {'rating': rating},
      success: function(data) {
        this.props.fetch();
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  render: function() {
    if (this.props.movie) {
    var image_url = this.props.movie.img_url;
    if(!image_url || image_url === "") {
      image_url = "http://i.imdb.com/images/nopicture/140x209/unknown.png";
    }
    return (
      <div>
      <a href={'/movie/' + this.props.movie.movie_id}>
      <h4>{this.props.movie.title}</h4>
      <img style={{height: '268px', width: '182px'}} src={image_url} />
      </a>
<IconRating onChange={this._ratingOnChange}
  toggledClassName="fa-2x fa fa-star " untoggledClassName="fa-2x fa fa-star-o"/>
      </div>
    );
  } else {
    return (<div />);
  }
  }
});

var MovieRecs = React.createClass({
  getInitialState: function() {
    return {
      movies: []
    };
  },
  _getMovies: function() {
    $.ajax({
      url: '/get_recommendations/' + this.props.user_id + '/',
      dataType: 'json',
      success: function(data) {
        this.setState({'movies': data});

      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  componentDidMount: function() {
    this._getMovies();
  },
  componentWillReceiveProps: function(nextProps) {
    if (nextProps.fetchNew === true) {
      this._getMovies();
      this.props.unfetch();
      console.log('here');
    }
  },
  render: function() {
    return (
      <div style={{padding: '25px',backgroundColor: '#c0c0c0'}}>
      <h2>We Recommend: </h2>
     <div className="row">
      <div className="col-md-3">
      <RMovie user_id={this.props.user_id} fetch={this.props.fetch} movie={this.state.movies[0]}/>
      </div>
      <div className="col-md-3">
      <RMovie user_id={this.props.user_id} fetch={this.props.fetch} movie={this.state.movies[1]}/>
      </div>
            <div className="col-md-3">
      <RMovie user_id={this.props.user_id} fetch={this.props.fetch} movie={this.state.movies[2]}/>
      </div>
            <div className="col-md-3">
      <RMovie user_id={this.props.user_id} fetch={this.props.fetch} movie={this.state.movies[3]}/>
      </div>
      </div>
      </div>);
  }
});

var Movie = React.createClass({
  getInitialState: function() {
    return {
      fetch: false
    };
  },
  render: function() {
    return (
      <div className="container">
      <MovieRecs fetch={()=>this.setState({fetch: true})} fetchNew={this.state.fetch} unfetch={()=>{this.setState({fetch: false})}} user_id={this.props.user_id} />
            <div className="row">
      <div className="col-md-3">
      <MovieCell rid={16} sfetch={()=>this.setState({fetch: true})} user_id={this.props.user_id}/>
      </div>
      <div className="col-md-3">
      <MovieCell rid={15} fetch={()=>this.setState({fetch: true})} user_id={this.props.user_id}/>
      </div>
            <div className="col-md-3">
      <MovieCell rid={14} fetch={()=>this.setState({fetch: true})} user_id={this.props.user_id}/>
      </div>
            <div className="col-md-3">
      <MovieCell rid={13} fetch={()=>this.setState({fetch: true})} user_id={this.props.user_id}/>
      </div>
      </div>
                  <div className="row">
      <div className="col-md-3">
      <MovieCell rid={12} fetch={()=>this.setState({fetch: true})} user_id={this.props.user_id}/>
      </div>
      <div className="col-md-3">
      <MovieCell rid={11} fetch={()=>this.setState({fetch: true})} user_id={this.props.user_id}/>
      </div>
            <div className="col-md-3">
      <MovieCell rid={10} fetch={()=>this.setState({fetch: true})} user_id={this.props.user_id}/>
      </div>
            <div className="col-md-3">
      <MovieCell rid={9} fetch={()=>this.setState({fetch: true})} user_id={this.props.user_id}/>
      </div>
      </div>
                  <div className="row">
      <div className="col-md-3">
      <MovieCell rid={8} fetch={()=>this.setState({fetch: true})} user_id={this.props.user_id}/>
      </div>
      <div className="col-md-3">
      <MovieCell rid={7} fetch={()=>this.setState({fetch: true})} user_id={this.props.user_id}/>
      </div>
            <div className="col-md-3">
      <MovieCell rid={6} fetch={()=>this.setState({fetch: true})} user_id={this.props.user_id}/>
      </div>
            <div className="col-md-3">
      <MovieCell rid={5} fetch={()=>this.setState({fetch: true})} user_id={this.props.user_id}/>
      </div>
      </div>
                  <div className="row">
      <div className="col-md-3">
      <MovieCell rid={4} fetch={()=>this.setState({fetch: true})} user_id={this.props.user_id}/>
      </div>
      <div className="col-md-3">
      <MovieCell rid={3} fetch={()=>this.setState({fetch: true})} user_id={this.props.user_id}/>
      </div>
            <div className="col-md-3">
      <MovieCell rid={2} fetch={()=>this.setState({fetch: true})} user_id={this.props.user_id}/>
      </div>
            <div className="col-md-3">
      <MovieCell rid={1} fetch={()=>this.setState({fetch: true})} user_id={this.props.user_id}/>
      </div>
      </div>

      </div>
    );
  }
});


ReactDOM.render(
  <Movie user_id={myUserId}/>,
  document.getElementById('movie')
);