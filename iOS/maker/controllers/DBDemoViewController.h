//
//  DBDemoViewController.h
//  maker
//
//  Created by Bear on 2/23/14.
//  Copyright (c) 2014 Bear. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "DBTouchControl.h"

@interface DBDemoViewController : UIViewController<DBTouchControl>

@property (nonatomic, strong) NSString * api;
@property (nonatomic, strong) UIActivityIndicatorView * spinner;

-(id)initWithUrl:(NSString *)url;

@end
